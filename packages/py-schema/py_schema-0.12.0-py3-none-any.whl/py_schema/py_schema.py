import re


class SchemaValidationError(Exception):
    def __init__(self, code: str, path: str, node, extra=None):
        self.code = code
        self.path = path
        self.node = node
        self.extra = extra


class SchemaValidator:
    def __init__(self, schema, value):
        self.schema = schema
        self.value = value
        self.path = ['$root']
        self.is_valid = None

    def add_to_path(self, key: str):
        self.path.append(key)

    def pop_path(self):
        self.path.pop()

    def raise_error(self, code: str, node, extra=None):
        self.is_valid = False

        raise SchemaValidationError(
            code=code,
            path='.'.join(self.path),
            node=node,
            extra=extra
        )

    def validate(self):
        self.schema.value = self.value
        self.schema.ctx = self
        self.schema.validate()
        self.is_valid = True


class BaseField:
    def __init__(self, required: bool = True):
        self.required = required
        self.value: any = None
        self.ctx: SchemaValidator = None

    def validate_required(self):
        if self.required and self.value is None:
            self.raise_error('REQUIRED_VALUE')

    def validator(self):
        raise NotImplementedError()

    def validate(self):
        self.validate_required()
        self.validator()

    def raise_error(self, code: str, extra=None):
        self.ctx.raise_error(
            code=code,
            node=self,
            extra=extra
        )


class IntField(BaseField):
    def __init__(self, min: int = None, max: int = None, *args, **kwargs):
        super(IntField, self).__init__(*args, **kwargs)
        self.min = min
        self.max = max

    def validator(self):
        if type(self.value) is not int:
            self.raise_error(
                'INT_TYPE'
            )

        if self.min is not None and self.value < self.min:
            self.raise_error(
                'INT_MIN'
            )

        if self.max is not None and self.value > self.max:
            self.raise_error(
                'INT_MAX'
            )


class FloatField(BaseField):
    def __init__(self, min: float = None, max: float = None, *args, **kwargs):
        super(FloatField, self).__init__(*args, **kwargs)
        self.min = min
        self.max = max

    def validator(self):
        if type(self.value) is not float:
            self.raise_error(
                'FLOAT_TYPE'
            )

        if self.min is not None and self.value < self.min:
            self.raise_error(
                'FLOAT_MIN'
            )

        if self.max is not None and self.value > self.max:
            self.raise_error(
                'FLOAT_MAX'
            )


class StrField(BaseField):
    def __init__(self, min_length: int = None, max_length: int = None, *args, **kwargs):
        super(StrField, self).__init__(*args, *kwargs)
        self.min_length = min_length
        self.max_length = max_length

    def validator(self):
        if type(self.value) is not str:
            self.raise_error(
                'STR_TYPE'
            )

        if self.min_length is not None and len(self.value) < self.min_length:
            self.raise_error(
                'STR_MIN_LENGTH'
            )

        if self.max_length is not None and len(self.value) > self.max_length:
            self.raise_error(
                'STR_MAX_LENGTH'
            )


class BoolField(BaseField):
    def validator(self):
        if type(self.value) is not bool:
            self.raise_error(
                'BOOL_TYPE'
            )


class DictField(BaseField):
    def __init__(self, schema: dict, optional_props: [str] = [], strict: bool = False, *args, **kwargs):
        super(DictField, self).__init__(*args, **kwargs)
        self.schema = schema
        self.optional_props = optional_props
        self.strict = strict

    def validator(self):
        if type(self.value) is not dict:
            self.raise_error(
                'DICT_TYPE'
            )

        if self.strict:
            for value_prop_key in self.value:
                if value_prop_key not in self.schema and value_prop_key not in self.optional_props:
                    self.raise_error(
                        'DICT_PROP_NOT_ALLOWED',
                        extra={'prop': value_prop_key}
                    )

        for schema_prop_key in self.schema:
            if schema_prop_key not in self.value:
                if schema_prop_key in self.optional_props:
                    continue
                else:
                    self.raise_error(
                        'DICT_PROP_MISSING',
                        extra={'prop': schema_prop_key}
                    )

            prop_field = self.schema[schema_prop_key]

            self.ctx.add_to_path(schema_prop_key)

            prop_field.value = self.value[schema_prop_key]
            prop_field.ctx = self.ctx

            prop_field.validate()

            self.ctx.pop_path()


class ListField(BaseField):
    def __init__(self, item_schema: BaseField, min_items: int = None, max_items: int = None, *args, **kwargs):
        super(ListField, self).__init__(*args, **kwargs)
        self.item_schema = item_schema
        self.min_items = min_items
        self.max_items = max_items

    def validator(self):
        if type(self.value) is not list:
            self.raise_error(
                'LIST_TYPE'
            )

        if self.min_items is not None and len(self.value) < self.min_items:
            self.raise_error(
                'LIST_MIN_ITEMS'
            )

        if self.max_items is not None and len(self.value) > self.max_items:
            self.raise_error(
                'LIST_MAX_ITEMS'
            )

        for index, item in enumerate(self.value):
            self.ctx.add_to_path('${}'.format(index))

            self.item_schema.value = item
            self.item_schema.ctx = self.ctx
            self.item_schema.validate()

            self.ctx.pop_path()


class EnumField(BaseField):
    def __init__(self, accept: [any], *args, **kwargs):
        super(EnumField, self).__init__(*args, **kwargs)
        self.accept = accept

    def validator(self):
        if self.value not in self.accept:
            self.raise_error(
                'ENUM_VALUE_NOT_ACCEPT'
            )


class RegexField(BaseField):
    def __init__(self, regex, *args, **kwargs):
        super(RegexField, self).__init__(*args, **kwargs)
        self.regex = regex

    def validator(self):
        if not re.match(self.regex, self.value):
            self.raise_error(
                'REGEX_NOT_MATCH'
            )


class OrField(BaseField):
    def __init__(self, schemas: [BaseField], *args, **kwargs):
        super(OrField, self).__init__(*args, **kwargs)
        self.schemas = schemas

    def validator(self):
        value = self.value
        schemas = self.schemas

        errors = []

        for sc in schemas:
            try:
                validator = SchemaValidator(
                    schema=sc,
                    value=value
                )
                validator.validate()

                return
            except SchemaValidationError as sve:
                errors.append(sve)

        if len(schemas) == len(errors):
            self.raise_error(
                code='OR_NO_MATCHING_SCHEMA',
                extra={
                    'errors': errors
                }
            )


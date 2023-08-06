from unittest import TestCase

from py_schema import SchemaValidator, SchemaValidationError, \
    IntField, StrField, BoolField, FloatField, DictField, ListField, \
    EnumField, RegexField, OrField


class SchemaValidatorTest(TestCase):
    def test_required_with_none_should_raise_error(self):
        schema = IntField(
            required=True
        )
        value = None

        validator = SchemaValidator(
            schema=schema,
            value=value
        )

        try:
            validator.validate()
            self.fail()
        except SchemaValidationError as e:
            self.assertEqual(
                e.path, '$root'
            )
            self.assertEqual(
                e.code, 'REQUIRED_VALUE'
            )

    def test_raised_error_should_contain_node(self):
        age_field = IntField(min=18)

        schema = DictField(
            schema={
                'age': age_field
            }
        )

        value = {
            'age': 12
        }

        try:
            validator = SchemaValidator(schema, value)
            validator.validate()
            self.fail()
        except SchemaValidationError as err:
            self.assertEqual(
                err.node,
                age_field
            )

    def test_full_schema_should_pass(self):
        schema = ListField(
            min_items=1,
            max_items=3,
            item_schema=DictField(
                schema={
                    'name': StrField(
                        min_length=2,
                        max_length=50,
                    ),
                    'age': IntField(
                        min=0,
                        max=120
                    ),
                    'money': FloatField(
                        min=0.0,
                        max=999.9
                    ),
                    'alive': BoolField(),
                    'gender': EnumField(
                        accept=['M', 'F', 'O']
                    ),
                    'code': RegexField(regex='^([0-9]{3})'),
                    'doc': OrField(
                        schemas=[
                            RegexField(regex='[0-9]{3}\\.?[0-9]{3}\\.?[0-9]{3}\\-?[0-9]{2}'),  # cpf
                            RegexField(regex='[0-9]{2}\\.?[0-9]{3}\\.?[0-9]{3}\\/?[0-9]{4}\\-?[0-9]{2}')  # cnpj
                        ]
                    )
                },
                strict=True,
                optional_props=['gender', 'code', 'doc']
            )
        )

        value = [
            {
                'name': 'Batman',
                'age': 31,
                'money': 999.0,
                'alive': True,
                'gender': 'M',
                'code': '468',
                'doc': '759.425.730-85'
            },
            {
                'name': 'Superman',
                'age': 29,
                'money': 0.0,
                'alive': True,
                'doc': '31.035.254/0001-79'
            }
        ]

        validator = SchemaValidator(
            schema=schema,
            value=value
        )

        validator.validate()


class IntFieldTest(TestCase):
    def test_not_type_int_should_raise_error(self):
        schema = IntField(
            required=True
        )
        value = 'abc'

        validator = SchemaValidator(
            schema=schema,
            value=value
        )

        try:
            validator.validate()
            self.fail()
        except SchemaValidationError as e:
            self.assertEqual(
                e.path, '$root'
            )
            self.assertEqual(
                e.code, 'INT_TYPE'
            )

    def test_value_less_should_raise_error(self):
        schema = IntField(
            min=1
        )
        value = 0

        validator = SchemaValidator(
            schema=schema,
            value=value
        )

        try:
            validator.validate()
            self.fail()
        except SchemaValidationError as e:
            self.assertEqual(
                e.path, '$root'
            )
            self.assertEqual(
                e.code, 'INT_MIN'
            )

    def test_value_greater_should_raise_error(self):
        schema = IntField(
            max=1
        )
        value = 2

        validator = SchemaValidator(
            schema=schema,
            value=value
        )

        try:
            validator.validate()
            self.fail()
        except SchemaValidationError as e:
            self.assertEqual(
                e.path, '$root'
            )
            self.assertEqual(
                e.code, 'INT_MAX'
            )

    def test_valid_value_should_pass(self):
        schema = IntField(
            min=1,
            max=10
        )
        value = 5

        validator = SchemaValidator(
            schema=schema,
            value=value
        )

        validator.validate()


class StrFieldTest(TestCase):
    def test_invalid_type_should_raise_error(self):
        schema = StrField()
        value = 123

        validator = SchemaValidator(
            schema=schema,
            value=value
        )

        try:
            validator.validate()
            self.fail()
        except SchemaValidationError as e:
            self.assertEqual(
                e.path, '$root'
            )
            self.assertEqual(
                e.code, 'STR_TYPE'
            )

    def test_min_length_should_raise_error(self):
        schema = StrField(
            min_length=4
        )
        value = 'abc'

        validator = SchemaValidator(
            schema=schema,
            value=value
        )

        try:
            validator.validate()
            self.fail()
        except SchemaValidationError as e:
            self.assertEqual(
                e.path, '$root'
            )
            self.assertEqual(
                e.code, 'STR_MIN_LENGTH'
            )

    def test_max_length_should_raise_error(self):
        schema = StrField(
            max_length=4
        )
        value = 'abcde'

        validator = SchemaValidator(
            schema=schema,
            value=value
        )

        try:
            validator.validate()
            self.fail()
        except SchemaValidationError as e:
            self.assertEqual(
                e.path, '$root'
            )
            self.assertEqual(
                e.code, 'STR_MAX_LENGTH'
            )

    def test_valid_str_should_pass(self):
        schema = StrField(
            min_length=1,
            max_length=5
        )
        value = 'abcde'

        validator = SchemaValidator(
            schema=schema,
            value=value
        )

        validator.validate()


class BoolFieldTest(TestCase):
    def test_invalid_type_should_raise_error(self):
        schema = BoolField()
        value = 'abc'

        validator = SchemaValidator(
            schema=schema,
            value=value
        )

        try:
            validator.validate()
            self.fail()
        except SchemaValidationError as e:
            self.assertEqual(
                e.path, '$root'
            )
            self.assertEqual(
                e.code, 'BOOL_TYPE'
            )

    def test_valid_bool_should_pass(self):
        schema = BoolField()
        value = False

        validator = SchemaValidator(
            schema=schema,
            value=value
        )

        validator.validate()


class FloatFieldTest(TestCase):
    def test_not_type_float_should_raise_error(self):
        schema = FloatField()
        value = 'abc'

        validator = SchemaValidator(
            schema=schema,
            value=value
        )

        try:
            validator.validate()
            self.fail()
        except SchemaValidationError as e:
            self.assertEqual(
                e.path, '$root'
            )
            self.assertEqual(
                e.code, 'FLOAT_TYPE'
            )

    def test_value_less_should_raise_error(self):
        schema = FloatField(
            min=1
        )
        value = 0.0

        validator = SchemaValidator(
            schema=schema,
            value=value
        )

        try:
            validator.validate()
            self.fail()
        except SchemaValidationError as e:
            self.assertEqual(
                e.path, '$root'
            )
            self.assertEqual(
                e.code, 'FLOAT_MIN'
            )

    def test_value_greater_should_raise_error(self):
        schema = FloatField(
            max=1
        )
        value = 2.0

        validator = SchemaValidator(
            schema=schema,
            value=value
        )

        try:
            validator.validate()
            self.fail()
        except SchemaValidationError as e:
            self.assertEqual(
                e.path, '$root'
            )
            self.assertEqual(
                e.code, 'FLOAT_MAX'
            )

    def test_valid_value_should_pass(self):
        schema = FloatField(
            min=1,
            max=10
        )
        value = 5.0

        validator = SchemaValidator(
            schema=schema,
            value=value
        )

        validator.validate()


class DictFieldTest(TestCase):
    def test_invalid_type_should_raise_error(self):
        schema = DictField(
            schema={}
        )
        value = 'abc'

        validator = SchemaValidator(
            schema=schema,
            value=value
        )

        try:
            validator.validate()
            self.fail()
        except SchemaValidationError as e:
            self.assertEqual(
                e.path, '$root'
            )
            self.assertEqual(
                e.code, 'DICT_TYPE'
            )

    def test_missing_prop_should_raise_error(self):
        schema = DictField(
            schema={
                'foo': BoolField(),
                'bar': BoolField()
            }
        )
        value = {
            'foo': True
        }

        validator = SchemaValidator(
            schema=schema,
            value=value
        )

        try:
            validator.validate()
            self.fail()
        except SchemaValidationError as e:
            self.assertEqual(
                e.path, '$root'
            )
            self.assertEqual(
                e.code, 'DICT_PROP_MISSING'
            )
            self.assertEqual(
                e.extra,
                {'prop': 'bar'}
            )

    def test_not_allowed_prop_should_raise_error(self):
        schema = DictField(
            schema={
                'foo': BoolField(),
                'bar': BoolField()
            },
            strict=True
        )
        value = {
            'foo': True,
            'bar': False,
            'baz': None
        }

        validator = SchemaValidator(
            schema=schema,
            value=value
        )

        try:
            validator.validate()
            self.fail()
        except SchemaValidationError as e:
            self.assertEqual(
                e.path, '$root'
            )
            self.assertEqual(
                e.code, 'DICT_PROP_NOT_ALLOWED'
            )
            self.assertEqual(
                e.extra,
                {'prop': 'baz'}
            )

    def test_optional_prop_should_be_valid_if_not_present(self):
        schema = DictField(
            schema={
                'foo': BoolField(),
                'bar': BoolField()
            },
            strict=True,
            optional_props=['bar']
        )
        value = {
            'foo': True
        }

        validator = SchemaValidator(
            schema=schema,
            value=value
        )

        validator.validate()

    def test_prop_with_invalid_value_should_raise_error(self):
        schema = DictField(
            schema={
                'foo': BoolField(),
                'bar': BoolField()
            },
            strict=True
        )
        value = {
            'foo': True,
            'bar': 'abc'
        }

        validator = SchemaValidator(
            schema=schema,
            value=value
        )

        try:
            validator.validate()
            self.fail()
        except SchemaValidationError as e:
            self.assertEqual(
                e.path, '$root.bar'
            )
            self.assertEqual(
                e.code, 'BOOL_TYPE'
            )

    def test_nested_dict_with_invalid_prop_should_raise_error(self):
        schema = DictField(
            schema={
                'foo': BoolField(),
                'bar': DictField(
                    schema={
                        'baz': BoolField()
                    }
                )
            },
            strict=True
        )
        value = {
            'foo': True,
            'bar': {
                'baz': 123
            }
        }

        validator = SchemaValidator(
            schema=schema,
            value=value
        )

        try:
            validator.validate()
            self.fail()
        except SchemaValidationError as e:
            self.assertEqual(
                e.path, '$root.bar.baz'
            )
            self.assertEqual(
                e.code, 'BOOL_TYPE'
            )


class ListFieldTest(TestCase):
    def test_invalid_type_should_raise_error(self):
        schema = ListField(
            item_schema=BoolField()
        )
        value = 'abc'

        validator = SchemaValidator(
            schema=schema,
            value=value
        )

        try:
            validator.validate()
            self.fail()
        except SchemaValidationError as e:
            self.assertEqual(
                e.path, '$root'
            )
            self.assertEqual(
                e.code, 'LIST_TYPE'
            )

    def test_less_items_should_raise_error(self):
        schema = ListField(
            item_schema=BoolField(),
            min_items=1
        )
        value = []

        validator = SchemaValidator(
            schema=schema,
            value=value
        )

        try:
            validator.validate()
            self.fail()
        except SchemaValidationError as e:
            self.assertEqual(
                e.path, '$root'
            )
            self.assertEqual(
                e.code, 'LIST_MIN_ITEMS'
            )

    def test_more_items_should_raise_error(self):
        schema = ListField(
            item_schema=BoolField(),
            max_items=1
        )
        value = [True, False]

        validator = SchemaValidator(
            schema=schema,
            value=value
        )

        try:
            validator.validate()
            self.fail()
        except SchemaValidationError as e:
            self.assertEqual(
                e.path, '$root'
            )
            self.assertEqual(
                e.code, 'LIST_MAX_ITEMS'
            )

    def test_invalid_item_value_should_raise_error(self):
        schema = ListField(
            item_schema=BoolField()
        )
        value = [True, False, 'zelda']

        validator = SchemaValidator(
            schema=schema,
            value=value
        )

        try:
            validator.validate()
            self.fail()
        except SchemaValidationError as e:
            self.assertEqual(
                e.path, '$root.$2'
            )
            self.assertEqual(
                e.code, 'BOOL_TYPE'
            )

    def test_invalid_nested_list_item_value_should_raise_error(self):
        schema = ListField(
            item_schema=DictField(
                schema={
                    'values': ListField(
                        item_schema=BoolField()
                    )
                }
            )
        )
        value = [
            {
                'values': [True, False, 'Link']
            }
        ]

        validator = SchemaValidator(
            schema=schema,
            value=value
        )

        try:
            validator.validate()
            self.fail()
        except SchemaValidationError as e:
            self.assertEqual(
                e.path, '$root.$0.values.$2'
            )
            self.assertEqual(
                e.code, 'BOOL_TYPE'
            )


class EnumFieldTest(TestCase):
    def test_not_accepted_value_should_raise_error(self):
        schema = EnumField(
            accept=['123']
        )
        value = '456'

        validator = SchemaValidator(
            schema=schema,
            value=value
        )

        try:
            validator.validate()
            self.fail()
        except SchemaValidationError as e:
            self.assertEqual(
                e.path, '$root'
            )
            self.assertEqual(
                e.code, 'ENUM_VALUE_NOT_ACCEPT'
            )


class RegexFieldTest(TestCase):
    def test_not_match_should_raise_error(self):
        schema = RegexField('\\d{5}\\Z')

        value = '1234'

        validator = SchemaValidator(schema, value)

        try:
            validator.validate()
            self.fail()
        except SchemaValidationError as e:
            self.assertEqual(
                e.code, 'REGEX_NOT_MATCH'
            )

    def test_valid_regex_should_pass(self):
        schema = RegexField('\\d{5}\\Z')

        value = '12345'

        validator = SchemaValidator(schema, value)

        validator.validate()


class OrFieldTest(TestCase):
    def test_multiple_schema_error_should_raise_error(self):
        schema = OrField(
            schemas=[
                StrField(),
                IntField()
            ]
        )

        value = True

        validator = SchemaValidator(schema, value)

        try:
            validator.validate()
            self.fail()
        except SchemaValidationError as e:
            self.assertEqual(
                e.code, 'OR_NO_MATCHING_SCHEMA'
            )
            self.assertEqual(
                2,
                len(e.extra['errors'])
            )

    def test_one_valid_schema_should_pass(self):
        schema = OrField(
            schemas=[
                StrField(),
                BoolField(),
                IntField()
            ]
        )

        value = True

        validator = SchemaValidator(schema, value)
        validator.validate()

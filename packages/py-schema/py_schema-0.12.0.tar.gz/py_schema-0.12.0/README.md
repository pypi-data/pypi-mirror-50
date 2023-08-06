# py_schema

A simple and extensible schema validator.

![travis](https://travis-ci.org/benhurott/py_schema.svg?branch=master)
[![codecov](https://codecov.io/gh/benhurott/py_schema/branch/master/graph/badge.svg)](https://codecov.io/gh/benhurott/py_schema)

## Install

```
pip install py-schema
```

## Usage

```python
from py_schema import SchemaValidator, SchemaValidationError
from py_schema import DictField, ListField, StrField, IntField


schema = DictField(
    schema={
        'name': StrField(min_length=2, max_length=50),
        'age': IntField(min=0, max=130),
        'pets': ListField(
            min_items=1,
            item_schema=StrField()
        )
    }
)

value = {
    'name': 'Bruce',
    'age': 40,
    'pets': ['Billy', False]
}

try:
    validator = SchemaValidator(
        schema=schema,
        value=value
    )
    
    validator.validate()
    
except SchemaValidationError as err:
    print(err.code)  # STR_TYPE
    print(err.path)  # $root.pets.$1

```

You can check the complete list of errors in each field spec.


## Fields


### BaseField

This is the abstract field that all the fields inherit from.

It has some shared props that you can use in all fields.

#### required

If marked as `True` (default) and the value is `None`, it will raise a `REQUIRED_VALUE` error.

```python
from py_schema import SchemaValidator, SchemaValidationError, StrField

try:
    schema = StrField(required=True)
    value = None
    
    validator = SchemaValidator(schema, value)
    validator.validate()
except SchemaValidationError as err:
    print(err.code)  # "REQUIRED_VALUE"

```


### IntField

Validate if the value is an integer.

```python
from py_schema import SchemaValidator, IntField


schema = IntField(
    min=1,
    max=100
)

value = 80

validator = SchemaValidator(schema, value)

validator.validate()
```

#### min (int, optional, default None)

If provided, it will validate if the value is >= of the `min`.

If not, it will raise a `INT_MIN` error.

#### max (int, optional, default None)

If provided, it will validate if the value is <= of the `max`.

If not, it will raise a `INT_MAX` error.


### StrField

Validate if the value is a string.

```python
from py_schema import SchemaValidator, StrField


schema = StrField(
    min_length=2,
    max_length=50
)

value = 'Luca Turilli'

validator = SchemaValidator(schema, value)

validator.validate()

```

#### min_length (int, optional, default None)

If provided, it will validate if the string len is >= of the `min_length`.

If not, it will raise a `STR_MIN_LENGTH` error.


#### max_length (int, optional, default None)

If provided, it will validate if the string len is <= of the `max_length`.

If not, it will raise a `STR_MAX_LENGTH` error.


### FloatField

Validate if the value is a float.

```python
from py_schema import SchemaValidator, FloatField

schema = FloatField(
    min=0.0,
    max=99.0
)

value = 50.0

validator = SchemaValidator(schema, value)

validator.validate()

```

#### min (int, optional, default None)

If provided, it will validate if the value is >= of the `min`.

If not, it will raise a `FLOAT_MIN` error.

#### max (int, optional, default None)

If provided, it will validate if the value is <= of the `max`.

If not, it will raise a `FLOAT_MAX` error.


### BoolField

Validate if the value is a bool.

```python
from py_schema import SchemaValidator, BoolField

schema = BoolField()

value = False

validator = SchemaValidator(schema, value)

validator.validate()

```


### DictField

Validate if the value is a dict and each field inside it.

```python
from py_schema import SchemaValidator, DictField, StrField, BoolField


schema = DictField(
    schema={
        'name': StrField(),
        'admin': BoolField(),
        'contacts': DictField(
            schema={
                'phone': StrField(),
                'email': StrField()
            },
            optional_props=['phone']
        )
    },
    strict=True,
    optional_props=['contacts']
)

value = {
    'name': 'Dargor The Lord',
    'admin': True,
    'contacts': {
        'email': 'dargor@blackmountain.com'
    }
}

validator = SchemaValidator(schema, value)

validator.validate()
```

#### schema (dict, required)

The definition of the dictionary.


#### strict (bool, optional, default False)

If the schema should reject dictionary keys that is not present in the schema.

For example:

```python
from py_schema import SchemaValidator, SchemaValidationError, DictField, StrField, BoolField

try:
    schema = DictField(
        schema={
            'name': StrField(),
            'admin': BoolField()
        },
        strict=True
    )
    
    value = {
        'name': 'Dargor The Lord',
        'admin': True,
        'contacts': {
            'email': 'dargor@blackmountain.com'
        }
    }
    
    validator = SchemaValidator(schema, value)
    validator.validate()
    
except SchemaValidationError as err:
    print(err.code)  # DICT_PROP_NOT_ALLOWED
    print(err.extra)  # {'prop': 'contacts'}

```

In this case, the `contacts` property in the value is not present in the schema.

It will raise a `DICT_PROP_NOT_ALLOWED`.


#### optional_props ([str], optional, default [])

This prop indicates which properties are optional in schema.

If a prop is in this list and it's not in the value, it will be ignored.

Otherwise, it will raise a `DICT_PROP_MISSING` error.

Example:

```python
from py_schema import SchemaValidator, DictField, StrField, BoolField

schema = DictField(
    schema={
        'name': StrField(),
        'admin': BoolField(),
        'gender': StrField() 
    },
    optional_props=['gender']
)

value = {
    'name': 'Dargor The Lord',
    'admin': True
}

validator = SchemaValidator(schema, value)
validator.validate() # valid
```

```python
from py_schema import SchemaValidator, SchemaValidationError, DictField, StrField, BoolField

try:
    schema = DictField(
        schema={
            'name': StrField(),
            'admin': BoolField()
        }
    )
    
    value = {
        'name': 'Dargor The Lord'
    }
    
    validator = SchemaValidator(schema, value)
    validator.validate()
    
except SchemaValidationError as err:
    print(err.code)  # DICT_PROP_MISSING
    print(err.extra)  # {'prop': 'admin'}

```


### ListField

Validate if the value is a list and the items inside it.

```python
from py_schema import SchemaValidator, ListField, StrField


schema = ListField(
    min_items=1,
    max_items=3,
    item_schema=StrField()
)

value = ['Emerald', 'Sword']

validator = SchemaValidator(schema, value)
validator.validate()

```

#### item_schema (BaseField, required)

The schema for the item inside the list.


#### min_items (int, optional, default None)

Validate if the list contain at minimun `min_items` length.

If not, it will raise `LIST_MIN_ITEMS` error.


#### max_items (int, optional, default None)

Validate if the list contain at maximum `max_items` length.

If not, it will raise `LIST_MAX_ITEMS` error.



### EnumField

Validate if the value is one of the allowed values.


```python
from py_schema import SchemaValidator, EnumField


schema = EnumField(
    accept=[1, True, 'Immortal']
)

value = 1

validator = SchemaValidator(schema, value)
validator.validate()

```

#### accept (list, required)

The list of the values that can be accepted.

If the value is not in the `accepted`, it will raise a `ENUM_VALUE_NOT_ACCEPT` error.



### Regex Field

Validate if the value matches the regex.

```python
from py_schema import SchemaValidator, RegexField

schema = RegexField(regex='\\d{5}\\Z')

value = '12345'

validator = SchemaValidator(schema, value)

validator.validate()

```

#### regex (str, required)

The regex pattern.


### OR Field

Validate if the value matches with at least one of given schemas.

```python
from py_schema import OrField, StrField, BoolField, IntField, SchemaValidator, SchemaValidationError

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
except SchemaValidationError as e:
    print(e.extra['errors'])
```

#### schemas ([BaseField], required)

The list of the schemas to validate. 
If all the schemas failed, it will raise a `OR_NO_MATCHING_SCHEMA` error.

If the validation fail, you can check the error prop `extra['errors']` to see all the validation results.



## Misc

### SchemaValidationError

If a validation fails, it will raise a `SchemaValidationError`.

Inside the error will will have:

```python
from py_schema import SchemaValidationError

try:
    # ....
    pass
except SchemaValidationError as err:
    print(err.code)  # The code of the error
    print(err.path)  # The path in the schema that the error occurred.
    print(err.node)  # The BaseField node where the validation was raised.
    print(err.extra) # Any extra argument of the error.
```


## Creating custom validators

For better context, let's use this sample:

```python
from py_schema import DictField
from .my_field import MyField


schema = DictField(
    schema={
        'my_field': MyField()
    }
)

value = {
    'my_field': 'Avalon'
}

```

```python
from py_schema import BaseField


class MyField(BaseField):
    def validator(self):
        ctx = self.ctx # the current SchemaValidator instance
        value = self.value # here is the current value of the schema (in this sample: "Avalon")
        
        if value != 'Avalon': # create you custom validation
            self.raise_error( # if your validation fails, raise an error
                code='MY_CUSTOM_CODE',
                extra="Any other extra info for your error (optional)"
            )
```


And that's it =).
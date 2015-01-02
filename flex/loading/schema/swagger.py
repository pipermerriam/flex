from flex.constants import (
    STRING,
)
from flex.validation.common import (
    generate_object_validator,
    generate_type_validator,
)
from flex.validation.schema import (
    construct_schema_validators,
)


string_type_validator = generate_type_validator(STRING)

swagger_version_schema = {
    'enum': ['2.0'],
    'required': True,
    'type': STRING,
}

swagger_version_validators = construct_schema_validators(swagger_version_schema, {})

swagger_version_validator = generate_object_validator(swagger_version_validators)

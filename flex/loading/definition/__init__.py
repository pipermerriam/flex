from flex.datastructures import (
    ValidationDict,
)
from flex.constants import (
    OBJECT,
)
from flex.validation.common import (
    generate_object_validator,
)

from .schema_definitions import schema_definitions_validator


__ALL__ = [
    'schema_definitions_validator',
]

definitions_schema = {
    'type': OBJECT,
}


field_validators = ValidationDict()
field_validators.add_property_validator('definitions', schema_definitions_validator)


definitions_validator = generate_object_validator(
    schema=definitions_schema,
    field_validators=field_validators,
)

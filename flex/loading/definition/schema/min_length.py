from flex.constants import (
    INTEGER,
)
from flex.validation.common import (
    generate_object_validator,
)
from flex.validation.schema import (
    construct_schema_validators,
)


min_length_schema = {
    'type': INTEGER,
    'minimum': 0,
}
min_length_validators = construct_schema_validators(min_length_schema, {})
min_length_validator = generate_object_validator(min_length_validators)

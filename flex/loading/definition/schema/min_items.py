from flex.constants import (
    INTEGER,
)
from flex.validation.common import (
    generate_object_validator,
)
from flex.validation.schema import (
    construct_schema_validators,
)


min_items_schema = {
    'type': INTEGER,
    'minimum': 0,
}
min_items_validators = construct_schema_validators(min_items_schema, {})

min_items_validator = generate_object_validator(
    field_validators=min_items_validators,
)

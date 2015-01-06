from flex.constants import (
    BOOLEAN,
)
from flex.validation.common import (
    generate_object_validator,
)
from flex.validation.schema import (
    construct_schema_validators,
)


unique_items_schema = {
    'type': BOOLEAN,
}
unique_items_validators = construct_schema_validators(unique_items_schema, {})

unique_items_validator = generate_object_validator(
    field_validators=unique_items_validators,
)

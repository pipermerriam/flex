from flex.exceptions import ValidationError
from flex.error_messages import MESSAGES
from flex.constants import (
    INTEGER,
    EMPTY,
)
from flex.validation.common import (
    generate_object_validator,
)
from flex.validation.schema import (
    construct_schema_validators,
)
from flex.decorators import (
    pull_keys_from_obj,
)


@pull_keys_from_obj('minItems', 'maxItems')
def validate_max_items_less_than_or_equal_to_min_items(minItems, maxItems):
    if minItems is EMPTY or maxItems is EMPTY:
        return
    if not maxItems >= minItems:
        raise ValidationError(
            MESSAGES['max_items']['must_be_greater_than_min_items']
        )


max_items_schema = {
    'type': INTEGER,
}
max_items_validators = construct_schema_validators(max_items_schema, {})

max_items_validator = generate_object_validator(
    field_validators=max_items_validators,
)

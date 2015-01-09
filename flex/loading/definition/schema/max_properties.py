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


@pull_keys_from_obj('minProperties', 'maxProperties')
def validate_max_properties_is_greater_than_or_equal_to_min_properties(minProperties,
                                                                       maxProperties,
                                                                       **kwargs):
    if maxProperties is EMPTY or minProperties is EMPTY:
        return
    if not maxProperties >= minProperties:
        raise ValidationError(
            MESSAGES['max_properties']['must_be_greater_than_min_properties'],
        )


max_properties_schema = {
    'type': INTEGER,
    'minimum': 0,
}
max_properties_validators = construct_schema_validators(max_properties_schema, {})
max_properties_validator = generate_object_validator(
    field_validators=max_properties_validators,
)

from flex.error_messages import MESSAGES
from flex.exceptions import ValidationError
from flex.constants import (
    EMPTY,
    INTEGER,
)
from flex.validation.common import (
    generate_object_validator,
)
from flex.decorators import (
    pull_keys_from_obj,
)


@pull_keys_from_obj('minLength', 'maxLength')
def validate_max_length_greater_than_or_equal_to_min_length(minLength, maxLength):
    if minLength is EMPTY or maxLength is EMPTY:
        return

    if not maxLength >= minLength:
        raise ValidationError(
            MESSAGES['max_length']['must_be_greater_than_min_length']
        )


max_length_schema = {
    'type': INTEGER,
    'minimum': 1,
}
max_length_validator = generate_object_validator(
    schema=max_length_schema,
)

from flex.exceptions import ValidationError
from flex.error_messages import MESSAGES
from flex.constants import (
    NUMBER,
    EMPTY,
    BOOLEAN,
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


@pull_keys_from_obj('minimum', 'maximum')
def validate_maximum_is_gte_minimum(minimum, maximum):
    if minimum is EMPTY or maximum is EMPTY:
        return
    if not maximum >= minimum:
        raise ValidationError(MESSAGES['maximum']['must_be_greater_than_minimum'])


@pull_keys_from_obj('maximum', 'exclusiveMaximum')
def validate_maximum_required_if_exclusive_maximum_set(maximum, exclusiveMaximum):
    if exclusiveMaximum is EMPTY:
        return
    if exclusiveMaximum is True and maximum is EMPTY:
        raise ValidationError(
            MESSAGES['maximum']['exclusive_maximum_required_maximum'],
        )


maximum_schema = {
    'type': NUMBER,
}
maximum_validators = construct_schema_validators(maximum_schema, {})
maximum_validator = generate_object_validator(maximum_validators)

exclusive_maximum_schema = {
    'type': BOOLEAN,
}
exclusive_maximum_validators = construct_schema_validators(exclusive_maximum_schema, {})
exclusive_maximum_validator = generate_object_validator(
    field_validators=exclusive_maximum_validators,
)

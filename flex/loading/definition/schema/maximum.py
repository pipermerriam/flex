from flex.exceptions import ValidationError
from flex.error_messages import MESSAGES
from flex.constants import (
    NUMBER,
    EMPTY,
)
from flex.validation.common import (
    generate_object_validator,
)
from flex.validation.schema import (
    construct_schema_validators,
)


def validate_maximum_is_gte_minimum(obj):
    minimum = obj.get('minimum', EMPTY)
    maximum = obj.get('maximum', EMPTY)
    if minimum is EMPTY:
        return
    if maximum is EMPTY:
        return
    if not maximum >= minimum:
        raise ValidationError(MESSAGES['maximum']['must_be_greater_than_minimum'])


def validate_maximum_required_if_exclusive_maximum_set(obj):
    maximum = obj.get('maximum', EMPTY)
    exclusive_maximum = obj.get('exclusiveMaximum', EMPTY)
    if exclusive_maximum is EMPTY:
        return
    if exclusive_maximum is True and maximum is EMPTY:
        raise ValidationError(
            MESSAGES['maximum']['exclusive_maximum_required_maximum'],
        )


maximum_schema = {
    'type': NUMBER,
}
maximum_validators = construct_schema_validators(maximum_schema, {})
maximum_validator = generate_object_validator(maximum_validators)

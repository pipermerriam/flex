from flex.exceptions import ValidationError
from flex.constants import (
    NUMBER,
    EMPTY,
)
from flex.error_messages import MESSAGES
from flex.validation.common import (
    generate_object_validator,
)
from flex.validation.schema import (
    construct_schema_validators,
)


def validate_minimum_required_if_exclusive_minimum_set(obj):
    minimum = obj.get('minimum', EMPTY)
    exclusive_minimum = obj.get('exclusiveMinimum', EMPTY)
    if exclusive_minimum is EMPTY:
        return
    if exclusive_minimum is True and minimum is EMPTY:
        raise ValidationError(
            MESSAGES['minimum']['exclusive_minimum_required_minimum'],
        )


minimum_schema = {
    'type': NUMBER,
}
minimum_validators = construct_schema_validators(minimum_schema, {})
minimum_validator = generate_object_validator(minimum_validators)

from flex.exceptions import ValidationError
from flex.constants import (
    NUMBER,
    EMPTY,
    BOOLEAN,
)
from flex.error_messages import MESSAGES
from flex.validation.common import (
    generate_object_validator,
)
from flex.validation.schema import (
    construct_schema_validators,
)
from flex.decorators import (
    pull_keys_from_obj,
)


@pull_keys_from_obj('minimum', 'exclusiveMinimum')
def validate_minimum_required_if_exclusive_minimum_set(minimum, exclusiveMinimum):
    if exclusiveMinimum is EMPTY:
        return
    if exclusiveMinimum is True and minimum is EMPTY:
        raise ValidationError(
            MESSAGES['minimum']['exclusive_minimum_required_minimum'],
        )


minimum_schema = {
    'type': NUMBER,
}
minimum_validators = construct_schema_validators(minimum_schema, {})
minimum_validator = generate_object_validator(
    field_validators=minimum_validators,
)

exclusive_minimum_schema = {
    'type': BOOLEAN,
}
exclusive_minimum_validators = construct_schema_validators(exclusive_minimum_schema, {})
exclusive_minimum_validator = generate_object_validator(
    field_validators=exclusive_minimum_validators,
)

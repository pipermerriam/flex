from flex.constants import (
    ARRAY,
    SCHEMES,
)
from flex.exceptions import ValidationError
from flex.error_messages import MESSAGES
from flex.validation.common import (
    generate_object_validator,
)
from flex.decorators import (
    skip_if_empty,
    skip_if_not_of_type,
)
from flex.validation.schema import (
    construct_schema_validators,
)


@skip_if_empty
@skip_if_not_of_type(ARRAY)
def _schemes_validator(schemes):
    for value in schemes:
        if value not in SCHEMES:
            raise ValidationError(
                MESSAGES['schemes']['invalid'].format(value),
            )


scheme_schema = {
    'type': ARRAY,
}

scheme_validators = construct_schema_validators(scheme_schema, {})
scheme_validators['value'] = _schemes_validator

schemes_validator = generate_object_validator(scheme_validators)

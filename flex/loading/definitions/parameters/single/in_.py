from flex.exceptions import ValidationError
from flex.error_messages import MESSAGES
from flex.constants import (
    STRING,
    PARAMETER_IN_VALUES,
    PATH,
)
from flex.validation.common import (
    generate_object_validator,
)
from flex.decorators import (
    pull_keys_from_obj,
    suffix_reserved_words,
    skip_if_any_kwargs_empty,
)


in_schema = {
    'type': STRING,
    'enum': PARAMETER_IN_VALUES,
    'required': True,
}


@pull_keys_from_obj('in', 'required')
@skip_if_any_kwargs_empty('in')
@suffix_reserved_words
def validate_path_parameters_must_be_required(in_, required, **kwargs):
    if in_ == PATH:
        if required is not True:
            raise ValidationError(MESSAGES['required']['path_parameters_must_be_required'])


in_validator = generate_object_validator(
    schema=in_schema,
)

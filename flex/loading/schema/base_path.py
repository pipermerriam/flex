from six.moves import urllib_parse as urlparse

from flex.constants import (
    STRING,
)
from flex.exceptions import ValidationError
from flex.error_messages import MESSAGES
from flex.validation.common import (
    generate_object_validator,
    generate_type_validator,
)
from flex.decorators import (
    skip_if_empty,
)
from flex.validation.schema import (
    construct_schema_validators,
)


string_type_validator = generate_type_validator(STRING)


@skip_if_empty
def path_validator(value):
    if not value.startswith('/'):
        raise ValidationError(MESSAGES['path']['must_start_with_slash'])
    parts = urlparse.urlparse(value)
    if value != parts.path:
        raise ValidationError(MESSAGES['path']['invalid'])


base_path_schema = {
    'type': STRING,
}

base_path_validators = construct_schema_validators(base_path_schema, {})
base_path_validators['value'] = path_validator

base_path_validator = generate_object_validator(base_path_validators)

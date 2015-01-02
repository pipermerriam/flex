import re

from flex.constants import (
    STRING,
    ARRAY,
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


# top-level type name / [ tree. ] subtype name [ +suffix ] [ ; parameters ]

TOP_LEVEL_TYPE_NAMES = set((
    'application',
    'audio',
    'example',
    'image',
    'message',
    'model',
    'multipart',
    'text',
    'video',
))


MIMETYPE_PATTERN = (
    '^'
    '(application|audio|example|image|message|model|multipart|text|video)'  # top-level type name
    '/'
    '(vnd(\.[-a-zA-Z0-9]+)*\.)?'  # vendor tree
    '([-a-zA-Z0-9]+)'  # media type
    '(\+(xml|json|ber|der|fastinfoset|wbxml|zip))?'
    '((; [-a-zA-Z0-9]+=(([-\.a-zA-Z0-9]+)|(("|\')[-\.a-zA-Z0-9]+("|\'))))+)?'  # parameters
    '$'
)


@skip_if_empty
@skip_if_not_of_type(ARRAY)
def _mimetype_validator(values):
    for value in values:
        if not re.match(MIMETYPE_PATTERN, value):
            raise ValidationError(
                MESSAGES['mimetype']['invalid'].format(value),
            )


mimetype_schema = {
    'type': ARRAY,
}

mimetype_validators = construct_schema_validators(mimetype_schema, {})
mimetype_validators['value'] = _mimetype_validator

mimetype_validator = generate_object_validator(mimetype_validators)

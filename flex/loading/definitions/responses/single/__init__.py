from flex.constants import (
    OBJECT,
    STRING,
)
from flex.validation.common import (
    generate_object_validator,
)


single_response_schema = {
    'type': OBJECT,
    'properties': {
        'description': {
            'type': STRING,
            'required': True,
        },
    },
}


single_response_validator = generate_object_validator(
    schema=single_response_schema,
)

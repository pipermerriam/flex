from flex.constants import (
    ARRAY,
    STRING,
    OBJECT,
)
from flex.validation.common import (
    generate_object_validator,
)


operation_schema = {
    'type': OBJECT,
    'properties': {
        'tags': {
            'type': ARRAY,
            'items': {
                'type': STRING,
            }
        }
    },
}


operation_validator = generate_object_validator(
    schema=operation_schema,
)

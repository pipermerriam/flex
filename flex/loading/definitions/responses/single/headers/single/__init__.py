from flex.constants import (
    OBJECT,
)
from flex.validation.common import (
    generate_object_validator,
)


single_header_schema = {
    'type': OBJECT,
}


single_header_validator = generate_object_validator(
    schema=single_header_schema,
)

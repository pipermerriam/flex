from flex.constants import (
    STRING,
    COLLECTION_FORMATS,
)
from flex.validation.common import (
    generate_object_validator,
)


collection_format_schema = {
    'type': STRING,
    'enum': COLLECTION_FORMATS,
}


collection_format_validator = generate_object_validator(
    schema=collection_format_schema,
)

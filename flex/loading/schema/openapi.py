from flex.constants import (
    STRING,
)
from flex.validation.common import (
    generate_object_validator,
)


openapi_version_schema = {
    'enum': ['3.0.0'],
    'type': STRING,
}

openapi_version_validator = generate_object_validator(
    schema=openapi_version_schema,
)

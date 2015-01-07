from flex.constants import (
    INTEGER,
)
from flex.validation.common import (
    generate_object_validator,
)


min_length_schema = {
    'type': INTEGER,
    'minimum': 0,
}
min_length_validator = generate_object_validator(
    schema=min_length_schema,
)

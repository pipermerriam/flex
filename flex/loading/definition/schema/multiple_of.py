from flex.constants import (
    NUMBER,
)
from flex.validation.common import (
    generate_object_validator,
)


multiple_of_schema = {
    'type': NUMBER,
    'minimum': 0,
}

multiple_of_validator = generate_object_validator(
    schema=multiple_of_schema,
)

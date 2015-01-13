from flex.constants import (
    BOOLEAN,
)
from flex.validation.common import (
    generate_object_validator,
)


required_schema = {
    'type': BOOLEAN,
}


required_validator = generate_object_validator(
    schema=required_schema,
)

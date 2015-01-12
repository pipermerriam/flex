from flex.constants import (
    STRING,
    PARAMETER_IN_VALUES,
)
from flex.validation.common import (
    generate_object_validator,
)


in_schema = {
    'type': STRING,
    'enum': PARAMETER_IN_VALUES,
    'required': True,
}


in_validator = generate_object_validator(
    schema=in_schema,
)

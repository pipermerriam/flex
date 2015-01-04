from flex.constants import (
    NUMBER,
)
from flex.validation.common import (
    generate_object_validator,
)
from flex.validation.schema import (
    construct_schema_validators,
)


maximum_schema = {
    'type': NUMBER,
}
maximum_validators = construct_schema_validators(maximum_schema, {})
maximum_validator = generate_object_validator(maximum_validators)

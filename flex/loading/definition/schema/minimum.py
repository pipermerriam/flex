from flex.constants import (
    NUMBER,
)
from flex.validation.common import (
    generate_object_validator,
)
from flex.validation.schema import (
    construct_schema_validators,
)


minimum_schema = {
    'type': NUMBER,
}
minimum_validators = construct_schema_validators(minimum_schema, {})
minimum_validator = generate_object_validator(minimum_validators)

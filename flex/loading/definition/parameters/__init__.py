import functools
from flex.datastructures import (
    ValidationList,
)
from flex.constants import (
    ARRAY,
    OBJECT,
)
from flex.validation.common import (
    generate_object_validator,
    apply_validator_to_array,
)


parameter_schema = {
    'type': OBJECT,
}

parameter_validator = generate_object_validator(
    schema=parameter_schema
)


parameters_schema = {
    'type': ARRAY,
}

parameters_non_field_validators = ValidationList()
parameters_non_field_validators.add_validator(
    functools.partial(apply_validator_to_array, parameter_validator),
)

parameters_validator = generate_object_validator(
    schema=parameters_schema,
    non_field_validators=parameters_non_field_validators,
)

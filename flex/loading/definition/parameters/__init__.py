import functools
from flex.datastructures import (
    ValidationList,
    ValidationDict,
)
from flex.constants import (
    ARRAY,
    OBJECT,
)
from flex.validation.common import (
    generate_object_validator,
    apply_validator_to_array,
)
from flex.loading.common import (
    field_validators as common_field_validators,
    non_field_validators as common_non_field_validators,
    type_validators as common_type_validators,
)
from flex.loading.definition.schema import (
    schema_validator,
    items_validator,
)


single_parameter_schema = {
    'type': OBJECT,
}

single_parameter_field_validators = ValidationDict()
single_parameter_field_validators.update(common_field_validators)

single_parameter_field_validators.add_property_validator('schema', schema_validator)
single_parameter_field_validators.add_property_validator('items', items_validator)

single_parameter_non_field_validators = ValidationDict()
single_parameter_non_field_validators.update(common_non_field_validators)
single_parameter_non_field_validators.update(common_type_validators)

single_parameter_validator = generate_object_validator(
    schema=single_parameter_schema,
    field_validators=single_parameter_field_validators,
    non_field_validators=single_parameter_non_field_validators,
)


parameters_schema = {
    'type': ARRAY,
}

parameters_non_field_validators = ValidationList()
parameters_non_field_validators.add_validator(
    functools.partial(apply_validator_to_array, single_parameter_validator),
)

parameters_validator = generate_object_validator(
    schema=parameters_schema,
    non_field_validators=parameters_non_field_validators,
)

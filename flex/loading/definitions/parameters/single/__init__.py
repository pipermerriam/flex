from flex.datastructures import (
    ValidationDict,
)
from flex.constants import (
    OBJECT,
)
from flex.loading.common import (
    field_validators as common_field_validators,
    non_field_validators as common_non_field_validators,
    type_validators as common_type_validators,
)
from flex.validation.common import (
    generate_object_validator,
)
from flex.loading.definitions.schema import (
    schema_validator,
    items_validator,
)

from .in_ import (
    in_validator,
)
from .name import (
    name_validator,
)


single_parameter_schema = {
    'type': OBJECT,
}

single_parameter_field_validators = ValidationDict()
single_parameter_field_validators.update(common_field_validators)

single_parameter_field_validators.add_property_validator('in', in_validator)
single_parameter_field_validators.add_property_validator('name', name_validator)
# schema fields
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

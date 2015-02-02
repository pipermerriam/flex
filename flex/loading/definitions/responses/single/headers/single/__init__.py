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
from .description import (
    description_validator,
)


single_header_schema = {
    'type': OBJECT,
}

single_header_field_validators = ValidationDict()
single_header_field_validators.update(common_field_validators)
single_header_field_validators.add_property_validator('schema', schema_validator)
single_header_field_validators.add_property_validator('items', items_validator)
single_header_field_validators.add_property_validator('description', description_validator)

single_header_non_field_validators = ValidationDict()
single_header_non_field_validators.update(common_non_field_validators)
single_header_non_field_validators.update(common_type_validators)

single_header_validator = generate_object_validator(
    schema=single_header_schema,
    field_validators=single_header_field_validators,
    non_field_validators=single_header_non_field_validators,
)

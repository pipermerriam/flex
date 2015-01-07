from flex.constants import (
    OBJECT,
)
from flex.decorators import (
    skip_if_not_of_type,
    skip_if_empty,
)
from flex.functional import (
    apply_functions_to_key,
)
from flex.validation.common import (
    generate_object_validator,
)
from flex.validation.schema import (
    construct_schema_validators,
)
from flex.datastructures import (
    ValidationDict,
)

from .multiple_of import multiple_of_validator
from .maximum import (
    maximum_validator,
    exclusive_maximum_validator,
    validate_maximum_is_gte_minimum,
    validate_maximum_required_if_exclusive_maximum_set,
)
from .minimum import (
    minimum_validator,
    exclusive_minimum_validator,
    validate_minimum_required_if_exclusive_minimum_set,
)
from .min_length import (
    min_length_validator,
)
from .max_length import (
    max_length_validator,
    validate_max_length_greater_than_or_equal_to_min_length,
)
from .pattern import (
    pattern_validator,
)
from .min_items import (
    min_items_validator,
)
from .max_items import (
    max_items_validator,
    validate_max_items_less_than_or_equal_to_min_items,
)
from .unique_items import (
    unique_items_validator,
)
from .enum import (
    enum_validator,
)
from .format import (
    format_validator,
)
from .title import (
    title_validator,
)
from .default import (
    validate_default_is_of_one_of_declared_types,
)
from .min_properties import (
    min_properties_validator,
)
from .max_properties import (
    max_properties_validator,
    validate_max_properties_is_greater_than_or_equal_to_min_properties,
)
from .required import (
    required_validator,
)
from .type import (
    type_validator,
)
from .read_only import (
    read_only_validator,
)

'''
    externalDocs = serializers.CharField(allow_null=True, required=False)
    # TODO: how do we do example
    # example =

    # Not Implemented
    # xml
    # discriminator
'''

schema_schema = {
    'type': OBJECT,
}
schema_validators = construct_schema_validators(schema_schema, {})

schema_validators.add_property_validator('multipleOf', multiple_of_validator)
schema_validators.add_property_validator('minimum', minimum_validator)
schema_validators.add_property_validator('maximum', maximum_validator)
schema_validators.add_property_validator('exclusiveMinimum', exclusive_minimum_validator)
schema_validators.add_property_validator('exclusiveMaximum', exclusive_maximum_validator)
schema_validators.add_property_validator('minLength', min_length_validator)
schema_validators.add_property_validator('maxLength', max_length_validator)
schema_validators.add_property_validator('pattern', pattern_validator)
schema_validators.add_property_validator('minItems', min_items_validator)
schema_validators.add_property_validator('maxItems', max_items_validator)
schema_validators.add_property_validator('uniqueItems', unique_items_validator)
schema_validators.add_property_validator('enum', enum_validator)
schema_validators.add_property_validator('format', format_validator)
schema_validators.add_property_validator('title', title_validator)
schema_validators.add_property_validator('minProperties', min_properties_validator)
schema_validators.add_property_validator('maxProperties', max_properties_validator)
schema_validators.add_property_validator('required', required_validator)
schema_validators.add_property_validator('type', type_validator)
schema_validators.add_property_validator('readOnly', read_only_validator)

non_field_validators = ValidationDict()
non_field_validators.add_validator(
    'maximum', validate_maximum_is_gte_minimum,
)
non_field_validators.add_validator(
    'maximum', validate_maximum_required_if_exclusive_maximum_set,
)
non_field_validators.add_validator(
    'minimum', validate_minimum_required_if_exclusive_minimum_set,
)
non_field_validators.add_validator(
    'maxLength', validate_max_length_greater_than_or_equal_to_min_length,
)
non_field_validators.add_validator(
    'maxItems', validate_max_items_less_than_or_equal_to_min_items,
)
non_field_validators.add_validator(
    'default', validate_default_is_of_one_of_declared_types,
)
non_field_validators.add_validator(
    'maxProperties', validate_max_properties_is_greater_than_or_equal_to_min_properties,
)

schema_validator = generate_object_validator(
    field_validators=schema_validators,
    non_field_validators=[non_field_validators],
)

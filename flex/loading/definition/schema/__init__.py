from flex.constants import (
    OBJECT,
    ARRAY,
    STRING,
)
from flex.exceptions import (
    ValidationError,
    ErrorDict,
    ErrorList,
)
from flex.utils import (
    is_value_of_type,
)
from flex.decorators import (
    skip_if_not_of_type,
    skip_if_empty,
)
from flex.validation.common import (
    generate_object_validator,
)
from flex.datastructures import (
    ValidationDict,
    ValidationList,
)

from .multiple_of import (
    multiple_of_validator,
    validate_type_for_multiple_of,
)
from .maximum import (
    maximum_validator,
    exclusive_maximum_validator,
    validate_maximum_is_gte_minimum,
    validate_maximum_required_if_exclusive_maximum_set,
    validate_type_for_maximum,
)
from .minimum import (
    minimum_validator,
    exclusive_minimum_validator,
    validate_minimum_required_if_exclusive_minimum_set,
    validate_type_for_minimum,
)
from .min_length import (
    min_length_validator,
    validate_type_for_min_length,
)
from .max_length import (
    max_length_validator,
    validate_max_length_greater_than_or_equal_to_min_length,
    validate_type_for_max_length,
)
from .pattern import (
    pattern_validator,
)
from .min_items import (
    min_items_validator,
    validate_type_for_min_items,
)
from .max_items import (
    max_items_validator,
    validate_max_items_less_than_or_equal_to_min_items,
    validate_type_for_max_items,
)
from .unique_items import (
    unique_items_validator,
    validate_type_for_unique_items,
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
from .ref import (
    ref_validator,
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

schema_field_validators = ValidationDict()

schema_field_validators.add_property_validator('multipleOf', multiple_of_validator)
schema_field_validators.add_property_validator('minimum', minimum_validator)
schema_field_validators.add_property_validator('maximum', maximum_validator)
schema_field_validators.add_property_validator('exclusiveMinimum', exclusive_minimum_validator)
schema_field_validators.add_property_validator('exclusiveMaximum', exclusive_maximum_validator)
schema_field_validators.add_property_validator('minLength', min_length_validator)
schema_field_validators.add_property_validator('maxLength', max_length_validator)
schema_field_validators.add_property_validator('pattern', pattern_validator)
schema_field_validators.add_property_validator('minItems', min_items_validator)
schema_field_validators.add_property_validator('maxItems', max_items_validator)
schema_field_validators.add_property_validator('uniqueItems', unique_items_validator)
schema_field_validators.add_property_validator('enum', enum_validator)
schema_field_validators.add_property_validator('format', format_validator)
schema_field_validators.add_property_validator('title', title_validator)
schema_field_validators.add_property_validator('minProperties', min_properties_validator)
schema_field_validators.add_property_validator('maxProperties', max_properties_validator)
schema_field_validators.add_property_validator('required', required_validator)
schema_field_validators.add_property_validator('type', type_validator)
schema_field_validators.add_property_validator('readOnly', read_only_validator)
schema_field_validators.add_property_validator('$ref', ref_validator)

schema_non_field_validators = ValidationDict()
schema_non_field_validators.add_validator(
    'type', validate_type_for_multiple_of,
)
schema_non_field_validators.add_validator(
    'maximum', validate_maximum_is_gte_minimum,
)
schema_non_field_validators.add_validator(
    'maximum', validate_maximum_required_if_exclusive_maximum_set,
)
schema_non_field_validators.add_validator(
    'type', validate_type_for_maximum,
)
schema_non_field_validators.add_validator(
    'minimum', validate_minimum_required_if_exclusive_minimum_set,
)
schema_non_field_validators.add_validator(
    'type', validate_type_for_minimum,
)
schema_non_field_validators.add_validator(
    'maxLength', validate_max_length_greater_than_or_equal_to_min_length,
)
schema_non_field_validators.add_validator(
    'type', validate_type_for_max_length,
)
schema_non_field_validators.add_validator(
    'type', validate_type_for_min_length,
)
schema_non_field_validators.add_validator(
    'maxItems', validate_max_items_less_than_or_equal_to_min_items,
)
schema_non_field_validators.add_validator(
    'type', validate_type_for_max_items,
)
schema_non_field_validators.add_validator(
    'type', validate_type_for_min_items,
)
schema_non_field_validators.add_validator(
    'type', validate_type_for_unique_items,
)
schema_non_field_validators.add_validator(
    'default', validate_default_is_of_one_of_declared_types,
)
schema_non_field_validators.add_validator(
    'maxProperties', validate_max_properties_is_greater_than_or_equal_to_min_properties,
)

schema_validator = generate_object_validator(
    schema=schema_schema,
    field_validators=schema_field_validators,
    non_field_validators=schema_non_field_validators,
)


#
# Properties.
#
@skip_if_empty
@skip_if_not_of_type(OBJECT)
def validate_properties(properties, **kwargs):
    with ErrorDict() as errors:
        for property_, value in properties.items():
            try:
                # TODO: this should be able to support a $ref
                schema_validator(value, **kwargs)
            except ValidationError as err:
                errors.add_error(property_, err.detail)


properties_schema = {
    'type': OBJECT,
}

properties_non_field_validators = ValidationDict()
properties_non_field_validators.add_validator('properties', validate_properties)

properties_validator = generate_object_validator(
    schema=properties_schema,
    non_field_validators=properties_non_field_validators,
)

# Now put the properties validator onto the schema validator.
schema_field_validators.add_property_validator('properties', properties_validator)


#
# Items
#
items_schema = {
    'type': [
        ARRAY,  # Array of schemas
        OBJECT,  # Single Schema
        STRING,  # Reference: TODO: verify this is the correct representation.
    ]
}


@skip_if_empty
@skip_if_not_of_type(ARRAY, OBJECT, STRING)
def validate_items(items, **kwargs):
    if is_value_of_type(OBJECT):
        schema_validator(items)
    elif is_value_of_type(STRING):
        # TODO: need ref support
        assert False, "Need support for $refs is not in yet"
    elif is_value_of_type(ARRAY):
        with ErrorList() as errors:
            for item in items:
                try:
                    schema_validator(item, **kwargs)
                except ValidationError as err:
                    errors.add_error(err.detail)
    else:
        raise ValueError("Unsupported type")


items_non_field_validators = ValidationList()
items_non_field_validators.add_validator(validate_items)

items_validator = generate_object_validator(
    schema=items_schema,
    non_field_validators=items_non_field_validators,
)

# Now put the items validator onto the schema validator
schema_field_validators.add_property_validator('items', items_validator)

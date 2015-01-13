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

from flex.loading.common.format import (
    format_validator,
)
from .title import (
    title_validator,
)
from flex.loading.common.default import (
    validate_default_is_of_one_of_declared_types,
)
from .min_properties import (
    min_properties_validator,
    validate_type_for_min_properties,
)
from .max_properties import (
    max_properties_validator,
    validate_max_properties_is_greater_than_or_equal_to_min_properties,
    validate_type_for_max_properties,
)
from flex.loading.common.required import (
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
from flex.loading.common import (
    field_validators as common_field_validators,
    non_field_validators as common_non_field_validators,
    type_validators as common_type_validators,
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
schema_field_validators.update(common_field_validators)

"""
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
"""
schema_field_validators.add_property_validator('format', format_validator)
schema_field_validators.add_property_validator('title', title_validator)
schema_field_validators.add_property_validator('minProperties', min_properties_validator)
schema_field_validators.add_property_validator('maxProperties', max_properties_validator)
schema_field_validators.add_property_validator('required', required_validator)
schema_field_validators.add_property_validator('type', type_validator)
schema_field_validators.add_property_validator('readOnly', read_only_validator)
schema_field_validators.add_property_validator('$ref', ref_validator)

schema_non_field_validators = ValidationDict()
schema_non_field_validators.update(common_non_field_validators)
schema_non_field_validators.update(common_type_validators)


schema_non_field_validators.add_validator(
    'default', validate_default_is_of_one_of_declared_types,
)
schema_non_field_validators.add_validator(
    'maxProperties', validate_max_properties_is_greater_than_or_equal_to_min_properties,
)
schema_non_field_validators.add_validator(
    'type', validate_type_for_min_properties,
)
schema_non_field_validators.add_validator(
    'type', validate_type_for_max_properties,
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

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
from .ref import (
    ref_validator,
)
from flex.loading.common.schema import (
    schema_schema as common_schema_schema,
    schema_field_validators as common_schema_field_validators,
    schema_non_field_validators as common_schema_non_field_validators,
    properties_schema as common_properties_schema,
    items_schema as common_items_schema,
)

schema_field_validators = ValidationDict()
schema_field_validators.update(common_schema_field_validators)

schema_field_validators.add_property_validator('$ref', ref_validator)

schema_non_field_validators = ValidationDict()
schema_non_field_validators.update(common_schema_non_field_validators)


schema_validator = generate_object_validator(
    schema=common_schema_schema,
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


properties_non_field_validators = ValidationDict()
properties_non_field_validators.add_validator('properties', validate_properties)

properties_validator = generate_object_validator(
    schema=common_properties_schema,
    non_field_validators=properties_non_field_validators,
)

# Now put the properties validator onto the schema validator.
schema_field_validators.add_property_validator('properties', properties_validator)


#
# Items
#
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
    schema=common_items_schema,
    non_field_validators=items_non_field_validators,
)

# Now put the items validator onto the schema validator
schema_field_validators.add_property_validator('items', items_validator)

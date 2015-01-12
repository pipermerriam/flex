from flex.datastructures import (
    ValidationList,
)
from flex.exceptions import (
    ValidationError,
    ErrorDict,
)
from flex.constants import OBJECT
from flex.decorators import (
    skip_if_empty,
    skip_if_not_of_type,
)
from flex.validation.common import (
    generate_object_validator,
)
from .schema import (
    schema_validator,
)


@skip_if_empty
@skip_if_not_of_type(OBJECT)
def validate_schema_definitions(definitions, **kwargs):
    with ErrorDict() as errors:
        for name, schema in definitions.items():
            try:
                schema_validator(schema, **kwargs)
            except ValidationError as err:
                errors.add_error(name, err.detail)


schema_definitions_schema = {
    'type': OBJECT,
}

non_field_validators = ValidationList()
non_field_validators.add_validator(validate_schema_definitions)

schema_definitions_validator = generate_object_validator(
    schema=schema_definitions_schema,
    non_field_validators=non_field_validators,
)

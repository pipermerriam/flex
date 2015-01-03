from flex.exceptions import ValidationError
from flex.constants import OBJECT
from flex.decorators import (
    skip_if_empty,
    skip_if_not_of_type,
)
from flex.validation.common import (
    generate_object_validator,
)
from flex.validation.schema import (
    construct_schema_validators,
)
from flex.context_managers import ErrorCollection


def schema_validator(*args, **kwargs):
    pass


@skip_if_empty
@skip_if_not_of_type(OBJECT)
def schema_definition_validator(definitions):
    with ErrorCollection() as errors:
        for name, schema in definitions.items():
            try:
                schema_validator(schema)
            except ValidationError as err:
                errors.add_error(name, err.detail)


schema_definitions_schema = {
    'type': OBJECT,
}

schema_definitions_validators = construct_schema_validators(schema_definitions_schema, {})
schema_definitions_validators['value'] = schema_definition_validator

schema_definitions_validator = generate_object_validator(schema_definitions_validators)

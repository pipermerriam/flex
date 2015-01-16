from flex.exceptions import ErrorDict
from flex.error_messages import MESSAGES
from flex.datastructures import (
    ValidationDict,
)
from flex.constants import (
    OBJECT,
)
from flex.validation.common import (
    generate_object_validator,
)
from flex.decorators import (
    skip_if_not_of_type,
    pull_keys_from_obj,
)

from .schema_definitions import schema_definitions_validator
from .parameters import (
    parameters_validator,
)
from .responses import (
    responses_validator,
)


__ALL__ = [
    'schema_definitions_validator',
    'parameters_validator',
    'responses_validator',
]

definitions_schema = {
    'type': OBJECT,
}


@skip_if_not_of_type(OBJECT)
@pull_keys_from_obj('definitions')
def validate_references(definitions, context, **kwargs):
    try:
        deferred_references = context['deferred_references']
    except:
        raise KeyError("`deferred_references` not found in context")

    with ErrorDict() as errors:
        for reference in deferred_references:
            if reference not in definitions:
                errors.add_error(
                    reference,
                    MESSAGES['reference']['undefined'].format(reference),
                )


field_validators = ValidationDict()
field_validators.add_property_validator('definitions', schema_definitions_validator)
field_validators.add_property_validator('parameters', parameters_validator)
field_validators.add_property_validator('responses', responses_validator)

non_field_validators = ValidationDict()
non_field_validators.add_validator('definitions', validate_references)


definitions_validator = generate_object_validator(
    schema=definitions_schema,
    field_validators=field_validators,
    non_field_validators=non_field_validators,
)

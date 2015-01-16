from flex.datastructures import (
    ValidationDict,
)
from flex.constants import (
    OBJECT,
    STRING,
)
from flex.validation.common import (
    generate_object_validator,
)
from flex.loading.definitions.schema import (
    schema_validator,
)
from .headers import (
    headers_validator,
)


single_response_schema = {
    'type': OBJECT,
    'properties': {
        'description': {
            'type': STRING,
            'required': True,
        },
    },
}


field_validators = ValidationDict()

field_validators.add_property_validator('schema', schema_validator)
field_validators.add_property_validator('headers', headers_validator)


single_response_validator = generate_object_validator(
    schema=single_response_schema,
    field_validators=field_validators,
)

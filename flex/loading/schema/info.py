from flex.constants import (
    STRING,
)
from flex.validation.common import (
    generate_object_validator,
    generate_type_validator,
)
from flex.validation.schema import (
    construct_schema_validators,
)


string_type_validator = generate_type_validator(STRING)

info_schema = {
    'required': True,
    'properties': {
        'title': {
            'required': True,
            'type': STRING,
        },
        'description': {'type': STRING},
        'termsOfService': {'type': STRING},
        'contact': {'type': STRING},
        'license': {'type': STRING},
        'version': {'type': STRING},
    }
}

info_validators = construct_schema_validators(info_schema, {})

info_validator = generate_object_validator(info_validators)

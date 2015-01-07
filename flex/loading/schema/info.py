from flex.constants import (
    STRING,
)
from flex.validation.common import (
    generate_object_validator,
)


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

info_validator = generate_object_validator(
    schema=info_schema,
)

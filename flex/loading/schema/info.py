from flex.constants import (
    STRING, OBJECT
)
from flex.validation.common import (
    generate_object_validator,
)


info_schema = {
    'required': [
        'title',
    ],
    'properties': {
        'title': {
            'type': STRING,
        },
        'description': {'type': STRING},
        'termsOfService': {'type': STRING},
        'contact': {'type': OBJECT},
        'license': {'type': STRING},
        'version': {'type': STRING},
    }
}

info_validator = generate_object_validator(
    schema=info_schema,
)

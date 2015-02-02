from flex.datastructures import (
    ValidationDict,
)
from flex.constants import (
    BOOLEAN,
    ARRAY,
    STRING,
    OBJECT,
)
from flex.validation.common import (
    generate_object_validator,
)
from flex.loading.common.mimetypes import (
    mimetype_validator,
)


operation_schema = {
    'type': OBJECT,
    'properties': {
        'tags': {
            'type': ARRAY,
            'items': {
                'type': STRING,
            }
        },
        'summary': {
            'type': STRING,
        },
        'description': {
            'type': STRING,
        },
        'externalDocs': {
            'type': STRING,
        },
        'operationId': {
            'type': STRING,
        },
        'consumes': {
            'type': ARRAY,
            'items': {
                'type': STRING,
            },
        },
        'produces': {
            'type': ARRAY,
            'items': {
                'type': STRING,
            },
        },
        #'parameters':
        #'responses':
        #'schemes':
        'deprecated': {
            'type': BOOLEAN,
        },
        #'security':
    },
}


field_validators = ValidationDict()
field_validators.add_property_validator('consumes', mimetype_validator)
field_validators.add_property_validator('produces', mimetype_validator)


operation_validator = generate_object_validator(
    schema=operation_schema,
)

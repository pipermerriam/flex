from flex.datastructures import (
    ValidationDict,
)
from flex.constants import (
    OBJECT,
)
from flex.validation.common import (
    generate_object_validator,
)


schema_schema = {
    'type': OBJECT,
}


field_validators = ValidationDict()


non_field_validators = ValidationDict()


schema_validator = generate_object_validator(
    schema=schema_schema,
    field_validators=field_validators,
    non_field_validators=non_field_validators,
)

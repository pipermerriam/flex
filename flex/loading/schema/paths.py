from flex.datastructures import (
    ValidationDict,
    ValidationList,
)
from flex.exceptions import ValidationError
from flex.constants import (
    OBJECT,
)
from flex.error_messages import MESSAGES
from flex.decorators import (
    skip_if_not_of_type,
    skip_if_empty,
)
from flex.validation.common import (
    generate_object_validator,
)
from flex.context_managers import (
    ErrorCollection,
)


def operation_validator(*args, **kwargs):
    pass


def parameters_validator(*args, **kwargs):
    pass


path_schema = {
    'type': OBJECT,
    'required': True,
}

non_field_validators = ValidationDict()
non_field_validators.add_property_validator('get', operation_validator)
non_field_validators.add_property_validator('put', operation_validator)
non_field_validators.add_property_validator('post', operation_validator)
non_field_validators.add_property_validator('delete', operation_validator)
non_field_validators.add_property_validator('options', operation_validator)
non_field_validators.add_property_validator('head', operation_validator)
non_field_validators.add_property_validator('patch', operation_validator)
non_field_validators.add_property_validator('parameters_validator', parameters_validator)

path_validator = generate_object_validator(
    schema=path_schema,
    non_field_validators=non_field_validators,
)


@skip_if_empty
@skip_if_not_of_type(OBJECT)
def validate_paths(paths, **kwargs):
    with ErrorCollection() as errors:
        for path, path_definition in paths.items():
            if not path.startswith('/'):
                errors.add_error(path, MESSAGES['path']['must_start_with_slash'])

            try:
                path_validator(path_definition)
            except ValidationError as err:
                errors.add_error(path, err.detail)


paths_schema = {
    'required': True,
    'type': OBJECT,
}
non_field_validators = ValidationList()
non_field_validators.add_validator(validate_paths)

paths_validator = generate_object_validator(
    schema=paths_schema,
    non_field_validators=non_field_validators,
)

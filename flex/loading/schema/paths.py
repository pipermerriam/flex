import operator

from flex.exceptions import ValidationError
from flex.constants import (
    EMPTY,
    OBJECT,
)
from flex.utils import (
    chain_reduce_partial,
)
from flex.decorators import (
    skip_if_not_of_type,
    skip_if_empty,
)
from flex.validation.common import (
    generate_object_validator,
)
from flex.validation.schema import (
    construct_schema_validators,
)
from flex.context_managers import (
    ErrorCollection,
)


def operation_validator(*args, **kwargs):
    pass


def parameters_validator(*args, **kwargs):
    pass


path_validators = {
    'get': chain_reduce_partial(
        operator.methodcaller('get', 'get', EMPTY),
        operation_validator,
    ),
    'put': chain_reduce_partial(
        operator.methodcaller('get', 'put', EMPTY),
        operation_validator,
    ),
    'post': chain_reduce_partial(
        operator.methodcaller('get', 'post', EMPTY),
        operation_validator,
    ),
    'delete': chain_reduce_partial(
        operator.methodcaller('get', 'delete', EMPTY),
        operation_validator,
    ),
    'options': chain_reduce_partial(
        operator.methodcaller('get', 'options', EMPTY),
        operation_validator,
    ),
    'head': chain_reduce_partial(
        operator.methodcaller('get', 'head', EMPTY),
        operation_validator,
    ),
    'patch': chain_reduce_partial(
        operator.methodcaller('get', 'patch', EMPTY),
        operation_validator,
    ),
    'parameters': parameters_validator,
}
path_validator = generate_object_validator(path_validators)


@skip_if_empty
@skip_if_not_of_type(OBJECT)
def _path_validator(paths):
    with ErrorCollection() as errors:
        for path, path_definition in paths.items():
            try:
                path_validator(path_definition)
            except ValidationError as err:
                errors.add_error(path, err.detail)


paths_schema = {
    'required': True,
    'type': OBJECT,
}
paths_validators = construct_schema_validators(paths_schema)

paths_validator = generate_object_validator(paths_validators)

import operator

from flex.constants import (
    EMPTY,
)
from flex.utils import (
    chain_reduce_partial,
)
from flex.validation.common import (
    generate_object_validator,
)
from .info import info_validator
from .swagger import swagger_version_validator
from .host import host_validator
from .path import base_path_validator


__ALL__ = [
    'info_validator',
    'swagger_schema_validators',
]


swagger_schema_validators = {
    'info': chain_reduce_partial(
        operator.methodcaller('get', 'info', EMPTY),
        info_validator,
    ),
    'swagger': chain_reduce_partial(
        operator.methodcaller('get', 'swagger', EMPTY),
        swagger_version_validator,
    ),
    'host': chain_reduce_partial(
        operator.methodcaller('get', 'host', EMPTY),
        host_validator,
    ),
    'basePath': chain_reduce_partial(
        operator.methodcaller('get', 'basePath', EMPTY),
        base_path_validator,
    ),
}

swagger_schema_validator = generate_object_validator(swagger_schema_validators)

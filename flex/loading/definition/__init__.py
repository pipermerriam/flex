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

from .schema_definitions import schema_definitions_validator


__ALL__ = [
    'schema_definitions_validator',
]


definitions_validators = {
    'definitions': chain_reduce_partial(
        operator.methodcaller('get', 'definitions', EMPTY),
        schema_definitions_validator,
    ),
}

definitions_validator = generate_object_validator(definitions_validators)

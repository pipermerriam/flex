import operator

from flex.constants import EMPTY
from flex.utils import (
    chain_reduce_partial,
)
from flex.validation.common import (
    validate_required,
    generate_object_validator,
)

info_validators = {
    'required': validate_required,
}
info_validator = generate_object_validator(info_validators)


swagger_schema_validators = {
    'info': chain_reduce_partial(
        operator.methodcaller('get', 'info', EMPTY),
        info_validator,
    ),
}

swagger_schema_validator = generate_object_validator(swagger_schema_validator)

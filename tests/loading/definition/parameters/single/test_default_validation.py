import pytest

from flex.error_messages import MESSAGES
from flex.exceptions import ValidationError
from flex.loading.definitions.parameters import (
    single_parameter_validator,
)

from tests.factories import ParameterFactory
from tests.utils import (
    assert_path_not_in_errors,
    assert_message_in_errors,
)


def test_default_is_not_required():
    context = {'deferred_references': set()}
    parameter = ParameterFactory()
    assert 'default' not in parameter
    try:
        single_parameter_validator(parameter, context=context)
    except ValidationError as err:
        errors = err.detail
    else:
        errors = {}

    assert_path_not_in_errors(
        'default',
        errors
    )


def test_parameter_validation_with_default_present():
    context = {'deferred_references': set()}
    parameter = ParameterFactory(default='0')
    assert 'default' in parameter
    try:
        single_parameter_validator(parameter, context=context)
    except ValidationError as err:
        errors = err.detail
    else:
        errors = {}

    assert_path_not_in_errors(
        'default',
        errors
    )

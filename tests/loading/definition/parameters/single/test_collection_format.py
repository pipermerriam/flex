import pytest

from flex.constants import (
    CSV,
)
from flex.error_messages import MESSAGES
from flex.exceptions import ValidationError
from flex.loading.definitions.parameters import (
    single_parameter_validator,
)

from tests.utils import (
    assert_path_not_in_errors,
    assert_message_in_errors,
)
from tests.factories import ParameterFactory


def test_collection_format_is_not_required():
    context = {'deferred_references': set()}

    try:
        single_parameter_validator({})
    except ValidationError as err:
        errors = err.detail
    else:
        errors = {}

    assert_path_not_in_errors(
        'collectionFormat',
        errors,
    )


def test_collection_format_defaults_to_csv():
    context = {'deferred_references': set()}

    raw_parameter = ParameterFactory()
    raw_parameter.pop('collectionFormat', None)
    value = single_parameter_validator(raw_parameter)

    with pytest.raises(AssertionError):
        # TODO: how do we set a default in the return object.
        assert value.get('collectionFormat') == CSV


@pytest.mark.parametrize(
    'value',
    ([1, 2], None, {'a': 1}, True, 1, 1.1),
)
def test_collection_format_with_invalid_types(value):
    with pytest.raises(ValidationError) as err:
        single_parameter_validator({'collectionFormat': value})

    assert_message_in_errors(
        MESSAGES['type']['invalid'],
        err.value.detail,
        'collectionFormat.type',
    )


def test_collection_format_with_invalid_value():
    with pytest.raises(ValidationError) as err:
        single_parameter_validator({'collectionFormat': 'not-a-collection-format'})

    assert_message_in_errors(
        MESSAGES['enum']['invalid'],
        err.value.detail,
        'collectionFormat.enum',
    )


def test_collection_format_with_valid_values():
    try:
        single_parameter_validator({'collectionFormat': CSV})
    except ValidationError as err:
        errors = err.detail
    else:
        errors = {}

    assert_path_not_in_errors(
        'collectionFormat',
        errors,
    )

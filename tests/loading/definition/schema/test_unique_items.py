import pytest

from flex.error_messages import MESSAGES
from flex.exceptions import ValidationError
from flex.loading.definition.schema import schema_validator

from tests.utils import (
    assert_path_not_in_errors,
    assert_message_in_errors,
)


def test_unique_items_are_not_required():
    try:
        schema_validator({})
    except ValidationError as err:
        errors = err.detail
    else:
        errors = {}

    assert_path_not_in_errors('uniqueItems', errors)


@pytest.mark.parametrize(
    'value',
    ([1, 2], None, {'a': 1}, 1, 1.1, 'abc'),
)
def test_unique_items_with_invalid_types(value):
    with pytest.raises(ValidationError) as err:
        schema_validator({'uniqueItems': value})

    assert_message_in_errors(
        MESSAGES['type']['invalid'],
        err.value.detail,
        'uniqueItems.type',
    )


def test_unique_items_with_valid_value():
    try:
        schema_validator({'uniqueItems': True})
    except ValidationError as err:
        errors = err.detail
    else:
        errors = {}

    assert_path_not_in_errors('uniqueItems', errors)

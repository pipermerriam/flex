import pytest

from flex.error_messages import MESSAGES
from flex.exceptions import ValidationError
from flex.loading.definition.schema import schema_validator

from tests.utils import (
    assert_path_not_in_errors,
    assert_message_in_errors,
)


def test_multiple_of_is_not_required():
    try:
        schema_validator({})
    except ValidationError as err:
        errors = err.detail
    else:
        errors = {}

    assert_path_not_in_errors('type', errors)


@pytest.mark.parametrize(
    'value',
    ('abc', [1, 2], None, {'a': 1}),
)
def test_multiple_of_for_invalid_types(value):
    with pytest.raises(ValidationError) as err:
        schema_validator({'multipleOf': value})

    assert_message_in_errors(
        MESSAGES['type']['invalid'],
        err.value.detail,
        'multipleOf.type',
    )


@pytest.mark.parametrize(
    'value',
    (-1, -1.5),
)
def test_multiple_of_invalid_for_negative_numbers(value):
    with pytest.raises(ValidationError) as err:
        schema_validator({'multipleOf': value})

    assert_message_in_errors(
        MESSAGES['minimum']['invalid'],
        err.value.detail,
        'multipleOf.minimum',
    )


@pytest.mark.parametrize(
    'value',
    (1, 1.5),
)
def test_multiple_for_valid_values(value):
    try:
        schema_validator({'multipleOf': value})
    except ValidationError as err:
        errors = err.detail
    else:
        errors = {}

    assert_path_not_in_errors('multipleOf', errors)

import pytest

from flex.error_messages import MESSAGES
from flex.exceptions import ValidationError
from flex.loading.definition.schema import schema_validator

from tests.utils import (
    assert_path_not_in_errors,
    assert_message_in_errors,
)


def test_minimum_and_maximum_are_not_required():
    """
    Ensure that neither the `minimum` nor the `maximum` fields of a schema are
    required.
    """
    try:
        schema_validator({})
    except ValidationError as err:
        errors = err.detail
    else:
        errors = {}

    assert_path_not_in_errors('minimum', errors)
    assert_path_not_in_errors('maximum', errors)


@pytest.mark.parametrize(
    'value',
    ('abc', [1, 2], None, {'a': 1}),
)
def test_minimum_for_invalid_types(value):
    """
    Ensure that the value of `minimum` is validated to be numeric.
    """
    with pytest.raises(ValidationError) as err:
        schema_validator({'minimum': value})

    assert_message_in_errors(
        MESSAGES['type']['invalid'],
        err.value.detail,
        'minimum.type',
    )


@pytest.mark.parametrize(
    'value',
    ('abc', [1, 2], None, {'a': 1}),
)
def test_maximum_for_invalid_types(value):
    """
    Ensure that the value of `maximum` is validated to be numeric.
    """
    with pytest.raises(ValidationError) as err:
        schema_validator({'maximum': value})

    assert_message_in_errors(
        MESSAGES['type']['invalid'],
        err.value.detail,
        'maximum.type',
    )


def test_minimum_is_required_if_exclusive_provided():
    """
    Ensure that when `exclusiveMinimum` is set, that `minimum` is required.
    """
    assert False


def test_maximum_is_required_if_exclusive_provided():
    """
    Ensure that when `exclusiveMaximum` is set, that `maximum` is required.
    """
    assert False


def test_maximum_must_be_greater_than_minimum():
    """
    Test that the maximum value must be greater than or equal to the minimum.
    """
    with pytest.raises(ValidationError) as err:
        schema_validator({
            'maximum': 10,
            'minimum': 11,
        })

    assert_message_in_errors(
        MESSAGES['maximum']['must_be_greater_than_minimum'],
        err.value.detail,
        'maximum',
    )

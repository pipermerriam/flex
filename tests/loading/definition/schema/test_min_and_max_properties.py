import pytest

from flex.error_messages import MESSAGES
from flex.exceptions import ValidationError
from flex.loading.definition.schema import schema_validator

from tests.utils import (
    assert_path_not_in_errors,
    assert_message_in_errors,
)


def test_min_and_max_properties_are_not_required():
    try:
        schema_validator({})
    except ValidationError as err:
        errors = err.detail
    else:
        errors = {}

    assert_path_not_in_errors('minProperties', errors)
    assert_path_not_in_errors('maxProperties', errors)


@pytest.mark.parametrize(
    'value',
    ('abc', [1, 2], None, {'a': 1}, True, False, 1.1),
)
def test_min_properties_for_invalid_types(value):
    """
    Ensure that the value of `minProperties` is validated to be numeric.
    """
    with pytest.raises(ValidationError) as err:
        schema_validator({'minProperties': value})

    assert_message_in_errors(
        MESSAGES['type']['invalid'],
        err.value.detail,
        'minProperties.type',
    )


@pytest.mark.parametrize(
    'value',
    ('abc', [1, 2], None, {'a': 1}, True, False, 1.1),
)
def test_max_properties_for_invalid_types(value):
    """
    Ensure that the value of `maxProperties` is validated to be numeric.
    """
    with pytest.raises(ValidationError) as err:
        schema_validator({'maxProperties': value})

    assert_message_in_errors(
        MESSAGES['type']['invalid'],
        err.value.detail,
        'maxProperties.type',
    )


def test_min_properties_must_be_greater_than_0():
    """
    Ensure that the value of `maxProperties` is validated to be numeric.
    """
    with pytest.raises(ValidationError) as err:
        schema_validator({'minProperties': -1})

    assert_message_in_errors(
        MESSAGES['minimum']['invalid'],
        err.value.detail,
        'minProperties.minimum',
    )


def test_max_properties_must_be_greater_than_0():
    """
    Ensure that the value of `maxProperties` is validated to be numeric.
    """
    with pytest.raises(ValidationError) as err:
        schema_validator({'maxProperties': -1})

    assert_message_in_errors(
        MESSAGES['minimum']['invalid'],
        err.value.detail,
        'maxProperties.minimum',
    )


def test_min_and_max_properties_with_valid_values():
    try:
        schema_validator({
            'minProperties': 4,
            'maxProperties': 8,
        })
    except ValidationError as err:
        errors = err.detail
    else:
        errors = {}

    assert_path_not_in_errors('minProperties', errors)
    assert_path_not_in_errors('maxProperties', errors)


def test_max_properties_must_be_greater_than_or_equal_to_min_properties():
    with pytest.raises(ValidationError) as err:
        schema_validator({
            'minProperties': 5,
            'maxProperties': 4,
        })

    assert_message_in_errors(
        MESSAGES['max_properties']['must_be_greater_than_min_properties'],
        err.value.detail,
        'maxProperties',
    )

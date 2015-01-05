import pytest

from flex.error_messages import MESSAGES
from flex.exceptions import ValidationError
from flex.loading.definition.schema import schema_validator

from tests.utils import (
    assert_path_not_in_errors,
    assert_message_in_errors,
)


def test_min_and_max_length_are_not_required():
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

    assert_path_not_in_errors('minLength', errors)
    assert_path_not_in_errors('maxLength', errors)


@pytest.mark.parametrize(
    'value',
    ('abc', [1, 2], None, {'a': 1}, True),
)
def test_min_length_for_invalid_types(value):
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

def test_more_things():
    assert False, "This suite is incomplete"

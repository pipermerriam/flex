import pytest

from flex.exceptions import (
    ValidationError,
)
from flex.error_messages import (
    MESSAGES,
)
from flex.constants import EMPTY

from tests.utils import (
    generate_validator_from_schema,
    assert_error_message_equal,
)


def test_field_declared_as_required():
    schema = {
        'required': True,
    }
    validator = generate_validator_from_schema(schema)

    with pytest.raises(ValidationError) as err:
        validator(EMPTY)

    assert 'required' in err.value.messages[0]
    assert_error_message_equal(
        err.value.messages[0]['required'][0],
        MESSAGES['required']['required'],
    )


def test_field_declared_as_required_with_field_present_is_valid():
    schema = {
        'required': True,
    }
    validator = generate_validator_from_schema(schema)

    validator('John Smith')

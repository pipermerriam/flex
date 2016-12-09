
import pytest

from flex.exceptions import ValidationError
from flex.constants import (
    STRING,
    INTEGER,
)
from flex.error_messages import MULTIPLE_OF_MESSAGES

from tests.utils import (
    generate_validator_from_schema,
    assert_message_in_errors
)


def test_oneof_simple():
    # example taken from http://spacetelescope.github.io/understanding-json-schema/reference/combining.html
    schema = {
        "oneOf": [
            { "type": INTEGER, "multipleOf": 5 },
            { "type": INTEGER, "multipleOf": 3 },
        ]
    }
    validator = generate_validator_from_schema(schema)

    validator(10)
    validator(9)


def test_one_of_complex_failure():
    # example taken from http://spacetelescope.github.io/understanding-json-schema/reference/combining.html
    schema = {
        "oneOf": [
            { "type": INTEGER, "multipleOf": 5 },
            { "type": INTEGER, "multipleOf": 3 },
        ]
    }
    validator = generate_validator_from_schema(schema)

    with pytest.raises(ValidationError) as err:
        validator(2)

    assert_message_in_errors(
        MULTIPLE_OF_MESSAGES['invalid'],
        err.value.detail,
    )

    with pytest.raises(ValidationError) as err:
        validator(15)

    assert_message_in_errors(
        MULTIPLE_OF_MESSAGES['invalid'],
        err.value.detail,
    )


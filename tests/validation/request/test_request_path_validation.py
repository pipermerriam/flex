import pytest

from flex.exceptions import ValidationError
from flex.validation.request import (
    validate_request,
)
from flex.error_messages import MESSAGES

from tests.factories import (
    SchemaFactory,
    RequestFactory,
)
from tests.utils import assert_message_in_errors


def test_request_validation_with_invalid_request_path():
    """
    Test that request validation detects request paths that are not declared
    in the schema.
    """
    schema = SchemaFactory()
    assert not schema['paths']

    request = RequestFactory(url='http://www.example.com/not-an-api-path')

    with pytest.raises(ValidationError) as err:
        validate_request(
            request,
            paths=schema['paths'],
            base_path=schema.get('base_path', ''),
            context=schema,
        )

    assert_message_in_errors(
        MESSAGES['path']['unknown_path'],
        err.value.detail,
        'path',
    )

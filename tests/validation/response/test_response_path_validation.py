import pytest

from flex.validation.response import (
    validate_response,
)
from flex.error_messages import MESSAGES

from tests.factories import (
    SchemaFactory,
    ResponseFactory,
)
from tests.utils import assert_error_message_equal


def test_response_validation_with_invalid_path():
    """
    Test that request validation detects request paths that are not declared
    in the schema.
    """
    from django.core.exceptions import ValidationError

    schema = SchemaFactory()
    assert not schema['paths']

    response = ResponseFactory(url='http://www.example.com/not-an-api-path')

    with pytest.raises(ValidationError) as err:
        validate_response(
            response,
            paths=schema['paths'],
            base_path=schema.get('base_path', ''),
            context=schema,
            inner=True,
        )

    assert 'path' in err.value.messages[0]
    assert_error_message_equal(
        err.value.messages[0]['path'][0],
        MESSAGES['path']['unknown_path'],
    )

import pytest

from flex.exceptions import ValidationError
from flex.validation.response import (
    validate_response,
)
from flex.error_messages import MESSAGES

from tests.factories import (
    SchemaFactory,
    ResponseFactory,
)
from tests.utils import (
    assert_message_in_errors,
)


def test_response_validation_with_invalid_path():
    """
    Test that request validation detects request paths that are not declared
    in the schema.
    """
    schema = SchemaFactory()
    assert not schema['paths']

    response = ResponseFactory(url='http://www.example.com/not-an-api-path')

    with pytest.raises(ValidationError) as err:
        validate_response(
            response=response,
            request_method='get',
            context=schema,
        )

    assert_message_in_errors(
        MESSAGES['path']['unknown_path'],
        err.value.detail,
        'path',
    )

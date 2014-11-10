import pytest

from flex.validation.response import (
    validate_api_call,
)
from flex.error_messages import MESSAGES

from tests.factories import (
    SchemaFactory,
    ResponseFactory,
)
from tests.utils import assert_error_message_equal


def test_response_validation_with_invalid_operation_on_path():
    """
    Test that response validation detects request paths that are not declared
    in the schema.
    """
    from django.core.exceptions import ValidationError

    schema = SchemaFactory(
        paths={
            '/post': {
                'post': None,
            },
        },
    )

    response = ResponseFactory(url='http://www.example.com/post')

    with pytest.raises(ValidationError) as err:
        validate_api_call(
            response,
            paths=schema['paths'],
            base_path=schema.get('base_path', ''),
            context=schema,
            inner=True,
        )

    assert 'request' in err.value.messages[0]
    assert_error_message_equal(
        err.value.messages[0]['request'][0],
        MESSAGES['request']['invalid_method'],
    )


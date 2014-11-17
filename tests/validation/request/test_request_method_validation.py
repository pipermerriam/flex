import pytest

from flex.validation.request import (
    validate_request,
)
from flex.error_messages import MESSAGES

from tests.factories import (
    SchemaFactory,
    RequestFactory,
)
from tests.utils import assert_error_message_equal


def test_request_validation_with_invalid_operation_on_path():
    """
    Test that request validation detects request paths that are not declared
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

    request = RequestFactory(url='http://www.example.com/post')

    with pytest.raises(ValidationError) as err:
        validate_request(
            request,
            paths=schema['paths'],
            base_path=schema.get('base_path', ''),
            context=schema,
            inner=True,
        )

    assert 'method' in err.value.messages[0]
    assert_error_message_equal(
        err.value.messages[0]['method'][0],
        MESSAGES['request']['invalid_method'],
    )


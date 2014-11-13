import pytest

from flex.validation.response import (
    validate_api_call,
)
from flex.error_messages import MESSAGES
from flex.constants import (
    INTEGER,
)

from tests.factories import (
    SchemaFactory,
    ResponseFactory,
)
from tests.utils import assert_error_message_equal


def test_response_header_validation():
    from django.core.exceptions import ValidationError

    schema = SchemaFactory(
        paths={
            '/get/': {
                'get': {
                    'responses': {200: {
                        'description': "Success",
                        'headers': {
                            'Foo': {'type': INTEGER},
                        }
                    }},
                },
            },
        },
    )

    response = ResponseFactory(
        url='http://www.example.com/get/',
        headers={'Foo': 'abc'},
    )

    with pytest.raises(ValidationError) as err:
        validate_api_call(
            response,
            paths=schema['paths'],
            base_path=schema.get('base_path', ''),
            context=schema,
            inner=True,
        )

    assert 'response' in err.value.messages[0]
    assert 'headers' in err.value.messages[0]['response'][0]
    assert 'Foo' in err.value.messages[0]['response'][0]['headers'][0]
    assert 'type' in err.value.messages[0]['response'][0]['headers'][0]['Foo'][0]
    assert_error_message_equal(
        err.value.messages[0]['response'][0]['headers'][0]['Foo'][0]['type'][0],
        MESSAGES['type']['invalid'],
    )

import pytest

from flex.exceptions import ValidationError
from flex.validation.response import (
    validate_response,
)
from flex.error_messages import MESSAGES
from flex.constants import (
    INTEGER,
    NUMBER,
    BOOLEAN,
    STRING,
)

from tests.factories import (
    SchemaFactory,
    ResponseFactory,
)
from tests.utils import assert_error_message_equal


def test_response_header_validation():
    """
    Test basic validation of response headers.
    """
    schema = SchemaFactory(
        paths={
            '/get': {
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
        url='http://www.example.com/get',
        headers={'Foo': 'abc'},
    )

    with pytest.raises(ValidationError) as err:
        validate_response(
            response,
            operation_definition=schema['paths']['/get']['get'],
            context=schema,
            inner=True,
        )

    assert 'body' in err.value.messages[0]
    assert 'headers' in err.value.messages[0]['body'][0]
    assert 'Foo' in err.value.messages[0]['body'][0]['headers'][0]
    assert 'type' in err.value.messages[0]['body'][0]['headers'][0]['Foo'][0]
    assert_error_message_equal(
        err.value.messages[0]['body'][0]['headers'][0]['Foo'][0]['type'][0],
        MESSAGES['type']['invalid'],
    )


@pytest.mark.parametrize(
    'type_,value',
    (
        (INTEGER, '3'),
        (NUMBER, '3.3'),
        (BOOLEAN, 'true'),
        (BOOLEAN, 'True'),
        (BOOLEAN, '1'),
        (BOOLEAN, 'false'),
        (BOOLEAN, 'False'),
        (BOOLEAN, '0'),
        (STRING, 'abcd'),
    )
)
def test_response_header_validation_for_non_strings(type_, value):
    schema = SchemaFactory(
        paths={
            '/get': {
                'get': {
                    'responses': {200: {
                        'description': "Success",
                        'headers': {
                            'Foo': {'type': type_},
                        }
                    }},
                },
            },
        },
    )

    response = ResponseFactory(
        url='http://www.example.com/get',
        headers={'Foo': value},
    )

    validate_response(
        response,
        operation_definition=schema['paths']['/get']['get'],
        context=schema,
        inner=True,
    )

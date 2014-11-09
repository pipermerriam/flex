import pytest

from flex.validation.response import (
    validate_response,
)
from flex.error_messages import MESSAGES
from flex.constants import (
    INTEGER,
    UUID,
    HEADER,
)

from tests.factories import (
    SchemaFactory,
    ResponseFactory,
)
from tests.utils import assert_error_message_equal


def test_request_header_validation():
    from django.core.exceptions import ValidationError

    schema = SchemaFactory(
        paths={
            '/get/': {
                'get': {
                    'responses': {200: {'description': "Success"}},
                    'parameters': [
                        {
                            'name': 'Authorization',
                            'in': HEADER,
                            'type': INTEGER,
                        }
                    ]
                },
            },
        },
    )

    response = ResponseFactory(
        url='http://www.example.com/get/',
        request__headers={'Authorization': 'abc'},
    )

    with pytest.raises(ValidationError) as err:
        validate_response(
            response,
            paths=schema['paths'],
            base_path=schema.get('base_path', ''),
            context=schema,
            inner=True,
        )

    assert 'request' in err.value.messages[0]
    assert 'parameters' in err.value.messages[0]['request'][0][0]
    assert 'headers' in err.value.messages[0]['request'][0][0]['parameters'][0]
    assert 'Authorization' in err.value.messages[0]['request'][0][0]['parameters'][0]['headers'][0]
    assert 'type' in err.value.messages[0]['request'][0][0]['parameters'][0]['headers'][0]['Authorization'][0]
    assert_error_message_equal(
        err.value.messages[0]['request'][0][0]['parameters'][0]['headers'][0]['Authorization'][0]['type'][0],
        MESSAGES['type']['invalid'],
    )

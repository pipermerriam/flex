import pytest

from flex.exceptions import ValidationError
from flex.validation.request import (
    validate_request,
)
from flex.error_messages import MESSAGES
from flex.constants import (
    PATH,
    QUERY,
    STRING,
    INTEGER,
)

from tests.factories import (
    SchemaFactory,
    RequestFactory,
)
from tests.utils import assert_error_message_equal


def test_request_parameter_validation():
    """
    Test that request validation does parameter validation.  This is largely a
    smoke test to ensure that parameter validation is wired into request
    validation correctly.
    """
    schema = SchemaFactory(
        paths={
            '/get/{id}/': {
                'parameters': [
                    {
                        'name': 'id',
                        'in': PATH,
                        'description': 'id',
                        'required': True,
                        'type': STRING,
                        'format': 'uuid',
                    },
                    {
                        'name': 'page',
                        'in': QUERY,
                        'type': INTEGER,
                    },
                ],
                'get': {
                    'responses': {200: {'description': "Success"}},
                },
            },
        },
    )

    request = RequestFactory(url='http://www.example.com/get/32/?page=abcd')

    with pytest.raises(ValidationError) as err:
        validate_request(
            request,
            paths=schema['paths'],
            base_path=schema.get('base_path', ''),
            context=schema,
            inner=True,
        )

    assert 'method' in err.value.messages[0]
    assert 'parameters' in err.value.messages[0]['method'][0]
    assert 'path' in err.value.messages[0]['method'][0]['parameters'][0]
    assert 'id' in err.value.messages[0]['method'][0]['parameters'][0]['path'][0]
    assert 'format' in err.value.messages[0]['method'][0]['parameters'][0]['path'][0]['id'][0]
    assert_error_message_equal(
        err.value.messages[0]['method'][0]['parameters'][0]['path'][0]['id'][0]['format'][0],
        MESSAGES['format']['invalid_uuid'],
    )

    assert 'query' in err.value.messages[0]['method'][0]['parameters'][0]
    assert 'page' in err.value.messages[0]['method'][0]['parameters'][0]['query'][0]
    assert 'type' in err.value.messages[0]['method'][0]['parameters'][0]['query'][0]['page'][0]
    assert_error_message_equal(
        err.value.messages[0]['method'][0]['parameters'][0]['query'][0]['page'][0]['type'][0],
        MESSAGES['type']['invalid'],
    )

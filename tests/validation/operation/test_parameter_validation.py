import pytest

from flex.validation.operation import (
    construct_operation_validators,
    validate_operation,
)
from flex.constants import (
    PATH,
    QUERY,
    STRING,
    INTEGER,
)
from flex.error_messages import MESSAGES

from tests.utils import assert_error_message_equal
from tests.factories import (
    RequestFactory,
    ResponseFactory,
    SchemaFactory,
)


#
#  path parameter validation.
#
def test_operation_parameter_validation_uses_correct_parameter_definitions():
    """
    Validation of a request's parameters involves merging the parameter
    definitions from the path definition as well as the operation definition.
    Ensure that this merging is happening and with the correct precendence to
    override path level parameters with any defined at the operation level.

    This test also serves as a *smoke* test to see that parameter validation is
    working as expected.
    """
    from django.core.exceptions import ValidationError
    schema = SchemaFactory(
        produces=['application/json'],
        paths={
            '/get/{username}/posts/{id}/': {
                'parameters': [
                    {
                        'name': 'username',
                        'in': PATH,
                        'description': 'username',
                        'required': True,
                        'type': STRING,
                    },
                    {
                        'name': 'id',
                        'in': PATH,
                        'description': 'id',
                        'required': True,
                        'type': INTEGER,
                    },
                ],
                'get': {
                    'responses': {200: {'description': 'Success'}},
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
                    ]
                },
            },
        },
    )

    url = 'http://www.example.com/get/fernando/posts/45/'

    response = ResponseFactory(
        request=RequestFactory(
            url=url,
        ),
        url=url,
    )
    api_path = '/get/{username}/posts/{id}/'
    path_definition = schema['paths']['/get/{username}/posts/{id}/']
    operation = response.request.method

    validators = construct_operation_validators(
        api_path=api_path,
        path_definition=path_definition,
        operation=operation,
        context=schema,
    )

    with pytest.raises(ValidationError) as err:
        validate_operation(response, validators, inner=True)

    assert 'parameters' in err.value.messages[0]
    assert 'path' in err.value.messages[0]['parameters'][0]
    assert 'id' in err.value.messages[0]['parameters'][0]['path'][0]
    assert 'format' in err.value.messages[0]['parameters'][0]['path'][0]['id'][0]
    assert_error_message_equal(
        err.value.messages[0]['parameters'][0]['path'][0]['id'][0]['format'][0],
        MESSAGES['format']['invalid_uuid'],
    )

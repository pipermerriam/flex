from flex.validation.response import (
    validate_response,
)

from tests.factories import (
    SchemaFactory,
    ResponseFactory,
)


def test_response_validation_with_invalid_operation_on_path():
    schema = SchemaFactory(
        produces=['application/json'],
        paths={
            '/get': {
                'get': {
                    'responses': {'200': {'description': 'Success'}},
                }
            },
        },
    )

    response = ResponseFactory(
        url='http://www.example.com/get',
        content_type=None,
    )

    validate_response(
        response=response,
        request_method='get',
        schema=schema,
    )


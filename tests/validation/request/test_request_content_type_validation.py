from flex.validation.request import (
    validate_request,
)

from tests.factories import (
    SchemaFactory,
    RequestFactory,
)


def test_request_validation_with_invalid_operation_on_path():
    schema = SchemaFactory(
        consumes=['application/json'],
        paths={
            '/get': {
                'get': {
                    'responses': {'200': {'description': 'Success'}},
                }
            },
        },
    )

    request = RequestFactory(
        url='http://www.example.com/get',
        content_type=None,
    )

    validate_request(
        request=request,
        schema=schema,
    )

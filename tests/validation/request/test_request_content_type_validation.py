import pytest

from flex.error_messages import MESSAGES
from flex.exceptions import ValidationError

from flex.validation.request import (
    validate_request,
)

from tests.factories import (
    SchemaFactory,
    RequestFactory,
)
from tests.utils import assert_message_in_errors


def test_request_content_type_validation():
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
        content_type='application/json',
    )

    validate_request(
        request=request,
        schema=schema,
    )


def test_request_content_type_validation_when_no_content_type_specified():
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

    with pytest.raises(ValidationError) as err:
        validate_request(
            request=request,
            schema=schema,
        )

    assert_message_in_errors(
        MESSAGES['content_type']['not_specified'],
        err.value.detail,
        'method.consumes',
    )


def test_request_content_type_validation_ignores_parameters():
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
        content_type='application/json; charset=utf-8',
    )

    validate_request(
        request=request,
        schema=schema,
    )

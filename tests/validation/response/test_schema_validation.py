import json
import pytest

from flex.exceptions import ValidationError
from flex.constants import (
    INTEGER,
    OBJECT,
    ARRAY,
    STRING,
)
from flex.validation.response import (
    validate_response,
)
from flex.error_messages import MESSAGES

from tests.factories import (
    SchemaFactory,
    ResponseFactory,
)
from tests.utils import assert_message_in_errors


def test_basic_response_body_schema_validation_with_invalid_value():
    schema = SchemaFactory(
        paths={
            '/get': {
                'get': {
                    'responses': {
                        200: {
                            'description': 'Success',
                            'schema': {'type': INTEGER},
                        }
                    },
                },
            },
        },
    )

    response = ResponseFactory(
        url='http://www.example.com/get',
        status_code=200,
        content_type='application/json',
        content=json.dumps('not-an-integer'),
    )

    with pytest.raises(ValidationError) as err:
        validate_response(
            response=response,
            request_method='get',
            schema=schema,
        )

    assert_message_in_errors(
        MESSAGES['type']['invalid'],
        err.value.detail,
        'body.schema.type',
    )


def test_basic_response_body_schema_validation_with_type_mismatch():
    """
    Ensure that when the expected response type is an object, and some other
    type is provided, that schema validation does not break since internally it
    will try to pull keys off of the value.
    """
    schema = SchemaFactory(
        paths={
            '/get': {
                'get': {
                    'responses': {
                        200: {
                            'description': 'Success',
                            'schema': {
                                'type': OBJECT,
                                'properties': {
                                    'id': {'type': INTEGER, 'required': True},
                                    'name': {'type': STRING, 'required': True},
                                },
                            },
                        }
                    },
                },
            },
        },
    )

    response = ResponseFactory(
        url='http://www.example.com/get',
        status_code=200,
        content_type='application/json',
        content=json.dumps([{'id': 3, 'name': 'Bob'}]),
    )

    with pytest.raises(ValidationError) as err:
        validate_response(
            response=response,
            request_method='get',
            schema=schema,
        )

    assert_message_in_errors(
        MESSAGES['type']['invalid'],
        err.value.detail,
        'body.schema.type',
    )


def test_response_body_schema_validation_with_items_as_reference():
    """
    Ensure that when the expected response type is an object, and some other
    type is provided, that schema validation does not break since internally it
    will try to pull keys off of the value.
    """
    schema = SchemaFactory(
        definitions={
            'User': {
                'properties': {
                    'id': {
                        'required': True,
                        'type': INTEGER,
                    },
                    'name': {
                        'required': True,
                        'enum': ('bob', 'joe'),
                    },
                },
            },
            'UserList': {
                'type': OBJECT,
                'properties': {
                    'results': {
                        'type': ARRAY,
                        'items': 'User',
                        'required': True,
                    },
                },
            },
        },
        paths={
            '/get': {
                'get': {
                    'responses': {
                        200: {
                            'description': 'Success',
                            'schema': {
                                '$ref': 'UserList',
                            },
                        }
                    },
                },
            },
        },
    )

    response = ResponseFactory(
        url='http://www.example.com/get',
        status_code=200,
        content_type='application/json',
        content=json.dumps({'results': [{'id': 3, 'name': 'billy'}]}),
    )

    with pytest.raises(ValidationError) as err:
        validate_response(
            response=response,
            request_method='get',
            schema=schema,
        )

    assert_message_in_errors(
        MESSAGES['type']['invalid'],
        err.value.detail,
        'body.schema.type',
    )

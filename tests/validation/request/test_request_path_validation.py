import pytest

from flex.serializers.core import PathsSerializer
from flex.validation.request import (
    validate_request,
    validate_request_to_path,
)
from flex.error_messages import MESSAGES
from flex.constants import (
    PATH,
    STRING,
    INTEGER,
)

from tests.factories import (
    SchemaFactory,
    RequestFactory,
)
from tests.utils import assert_error_message_equal


def test_request_validation_with_invalid_request_path():
    """
    Test that request validation detects request paths that are not declared
    in the schema.
    """
    from django.core.exceptions import ValidationError

    schema = SchemaFactory()
    assert not schema['paths']

    request = RequestFactory(url='http://www.example.com/not-an-api-path')

    with pytest.raises(ValidationError) as err:
        validate_request(
            request,
            paths=schema['paths'],
            base_path=schema.get('base_path', ''),
            context=schema,
            inner=True,
        )

    assert 'path' in err.value.messages[0]
    assert_error_message_equal(
        err.value.messages[0]['path'][0],
        MESSAGES['request']['unknown_path'],
    )


def test_basic_request_path_validation():
    serializer = PathsSerializer(data={
        '/get': None,
    })
    assert serializer.is_valid()

    paths = serializer.object

    request = RequestFactory(url='http://www.example.com/get')
    path, _ = validate_request_to_path(
        request,
        paths=paths,
        base_path='',
        context={},
    )
    assert path == '/get'


@pytest.mark.parametrize(
    'request_path',
    (
        '/get/',  # trailing slash.
        '/post',  # not declared at all
    )
)
def test_basic_request_path_validation_with_unspecified_paths(request_path):
    from django.core.exceptions import ValidationError
    serializer = PathsSerializer(data={
        '/get': None,
    })
    assert serializer.is_valid()

    paths = serializer.object

    url = 'http://www.example.com{0}'.format(request_path)

    request = RequestFactory(url=url)

    with pytest.raises(ValidationError):
        validate_request_to_path(
            request,
            paths=paths,
            base_path='',
            context={},
        )


def test_parametrized_string_path_validation():
    serializer = PathsSerializer(data={
        '/get/{id}': {
            'parameters': [
                # One very plain id of type string.
                {'name': 'id', 'in': PATH, 'description': 'The id', 'type': STRING, 'required': True},
            ],
        }
    })
    assert serializer.is_valid(), serializer.errors

    paths = serializer.object

    request = RequestFactory(url='http://www.example.com/get/25')
    path, _ = validate_request_to_path(
        request,
        paths=paths,
        base_path='',
        context={},
    )
    assert path == '/get/{id}'


def test_parametrized_integer_path_validation():
    serializer = PathsSerializer(data={
        '/get/{id}': {
            'parameters': [
                # One very plain id of type string.
                {'name': 'id', 'in': PATH, 'description': 'The id', 'type': INTEGER, 'required': True},
            ],
        }
    })
    assert serializer.is_valid(), serializer.errors

    paths = serializer.object

    request = RequestFactory(url='http://www.example.com/get/25')
    path, _ = validate_request_to_path(
        request,
        paths=paths,
        base_path='',
        context={},
    )
    assert path == '/get/{id}'


def test_parametrized_path_with_multiple_prameters():
    serializer = PathsSerializer(data={
        '/users/{username}/posts/{id}': {
            'parameters': [
                # One very plain id of type string.
                {'name': 'id', 'in': PATH, 'description': 'The id', 'type': INTEGER, 'required': True},
                {'name': 'username', 'in': PATH, 'description': 'The username', 'type': STRING, 'required': True},
            ],
        }
    })
    assert serializer.is_valid(), serializer.errors

    paths = serializer.object

    request = RequestFactory(url='http://www.example.com/users/john-smith/posts/47')
    path, _ = validate_request_to_path(
        request,
        paths=paths,
        base_path='',
        context={},
    )
    assert path == '/users/{username}/posts/{id}'

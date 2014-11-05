from flex.serializers.core import PathsSerializer
from flex.error_messages import MESSAGES
from flex.constants import (
    PATH,
    INTEGER,
)

from tests.utils import assert_error_message_equal

def test_paths_serializers_preserves_empty_paths():
    """
    Ensure that paths that are defined bare without any additional information
    are preserved in the paths serializer.
    """
    paths = {
        '/get': None,
        '/post': {'responses': None},
    }
    serializer = PathsSerializer(data=paths)

    assert serializer.is_valid()
    assert '/get' in serializer.object
    assert '/post' in serializer.object


def test_path_serializer_allows_parameters_that_are_not_defined():
    paths = {
        '/get/{id}/': None,
    }
    serializer = PathsSerializer(data=paths)

    assert serializer.is_valid()


def test_path_serializer_enforces_all_path_parameters_to_be_in_api_path():
    paths = {
        '/get/no-parameters/': {
            'parameters': [
                {
                    'name': 'id',
                    'in': PATH,
                    'description': 'id',
                    'type': INTEGER,
                    'required': True,
                },
            ],
        }
    }
    serializer = PathsSerializer(data=paths)

    assert not serializer.is_valid()
    assert 'non_field_errors' in serializer.errors
    assert '/get/no-parameters/' in serializer.errors['non_field_errors'][0]
    assert_error_message_equal(
        serializer.errors['non_field_errors'][0]['/get/no-parameters/'][0],
        MESSAGES['path']['missing_parameter'],
    )


def test_path_serializer_path_parameter_validation_handles_references():
    paths = {
        '/get/no-parameters/': {
            'parameters': [
                'Id',
            ],
        }
    }
    context = {
        'parameters': {
            'Id': {
                'name': 'id',
                'in': PATH,
                'description': 'id',
                'type': INTEGER,
                'required': True,
            },
        }
    }
    serializer = PathsSerializer(data=paths, context=context)

    assert not serializer.is_valid()
    assert 'non_field_errors' in serializer.errors
    assert '/get/no-parameters/' in serializer.errors['non_field_errors'][0]
    assert_error_message_equal(
        serializer.errors['non_field_errors'][0]['/get/no-parameters/'][0],
        MESSAGES['path']['missing_parameter'],
    )

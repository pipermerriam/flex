from flex.serializers.core import PathsSerializer
from flex.error_messages import MESSAGES

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


def test_path_serializer_enforces_path_parameters():
    paths = {
        '/get/{id}/': None,
    }
    serializer = PathsSerializer(data=paths)

    assert not serializer.is_valid()
    assert 'non_field_errors' in serializer.errors
    assert '/get/{id}/' in serializer.errors['non_field_errors'][0]
    assert_error_message_equal(
        serializer.errors['non_field_errors'][0]['/get/{id}/'][0],
        MESSAGES['path']['missing_parameter'],
    )

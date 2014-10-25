from flex.serializers.core import PathsSerializer


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

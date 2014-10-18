import pytest


def test_non_integer_type_raises_error():
    from flex.serializers.core import PropertiesSerializer

    schema = {
        'pk': {
            'type': 'integer',
        },
    }
    serializer = PropertiesSerializer(data=schema)
    assert serializer.is_valid()

    validator = serializer.save()

    with pytest.raises(ValueError):
        validator({'pk': '1'})


def test_string_type_raises_error():
    from flex.serializers.core import PropertiesSerializer

    schema = {
        'pk': {
            'type': 'integer',
        },
    }
    serializer = PropertiesSerializer(data=schema)
    assert serializer.is_valid()

    validator = serializer.save()

    with pytest.raises(ValueError):
        validator({'pk': 'abcd'})


def test_integer_type_valid():
    from flex.serializers.core import PropertiesSerializer
    schema = {
        'pk': {
            'type': 'integer',
        },
    }
    serializer = PropertiesSerializer(data=schema)
    assert serializer.is_valid()

    validator = serializer.save()

    validator({'pk': 1})

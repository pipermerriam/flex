import pytest

from rest_framework.serializers import ValidationError

from flex.serializers.core import PropertiesSerializer


def test_non_integer_type_raises_error():
    schema = {
        'pk': {
            'type': 'integer',
        },
    }
    serializer = PropertiesSerializer(data=schema)
    assert serializer.is_valid()

    validator = serializer.save()

    with pytest.raises(ValidationError):
        validator({'pk', '1'})


def test_string_type_raises_error():
    schema = {
        'pk': {
            'type': 'integer',
        },
    }
    serializer = PropertiesSerializer(data=schema)
    assert serializer.is_valid()

    validator = serializer.save()

    with pytest.raises(ValidationError):
        validator({'pk', 'abcd'})


def test_integer_type_valid():
    schema = {
        'pk': {
            'type': 'integer',
        },
    }
    serializer = PropertiesSerializer(data=schema)
    assert serializer.is_valid()

    validator = serializer.save()

    validator({'pk': 1})

import pytest

from flex.constants import (
    INTEGER,
    STRING,
)

from tests.utils import generate_validator_from_schema


#
# Integration style tests for PropertiesSerializer type validation.
#
def test_non_integer_type_raises_error():
    from flex.serializers.core import PropertiesSerializer

    schema = {
        'pk': {
            'type': INTEGER,
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
            'type': INTEGER,
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
            'type': INTEGER,
        },
    }
    serializer = PropertiesSerializer(data=schema)
    assert serializer.is_valid()

    validator = serializer.save()

    validator({'pk': 1})


@pytest.mark.parametrize(
    'value',
    (1, '1'),
)
def test_multi_type(value):
    from flex.serializers.core import PropertiesSerializer
    schema = {
        'pk': {
            'type': [INTEGER, STRING],
        },
    }
    serializer = PropertiesSerializer(data=schema)
    assert serializer.is_valid()

    validator = serializer.save()
    validator({'pk': value})


@pytest.mark.parametrize(
    'value',
    (None, True, False, [], {}),
)
def test_invalid_multi_type(value):
    from flex.serializers.core import PropertiesSerializer
    schema = {
        'pk': {
            'type': [INTEGER, STRING],
        },
    }
    serializer = PropertiesSerializer(data=schema)
    assert serializer.is_valid()

    validator = serializer.save()
    with pytest.raises(ValueError):
        validator({'pk': value})


def test_type_validation_is_noop_when_not_required_and_not_present():
    from flex.serializers.core import PropertiesSerializer
    schema = {
        'pk': {
            'type': [INTEGER, STRING],
        },
    }

    validator = generate_validator_from_schema(schema)

    validator({})

import pytest
from flex.constants import (
    INTEGER,
    NUMBER,
)

from tests.utils import generate_validator_from_schema

#
# Integration style tests for PropertiesSerializer type validation.
#
@pytest.mark.parametrize(
    'count',
    (-7, 0, 7, 14),
)
def test_integer_multiple_of(count):
    from flex.serializers.core import PropertiesSerializer

    schema = {
        'count': {
            'type': INTEGER,
            'multipleOf': 7,
        },
    }
    serializer = PropertiesSerializer(data=schema)
    assert serializer.is_valid(), serializer.errors

    validator = serializer.save()

    validator({'count': count})


@pytest.mark.parametrize(
    'count',
    (1, 2, 3, 9),
)
def test_integer_not_multiple_of(count):
    from flex.serializers.core import PropertiesSerializer

    schema = {
        'count': {
            'type': INTEGER,
            'multipleOf': 7,
        },
    }
    serializer = PropertiesSerializer(data=schema)
    assert serializer.is_valid(), serializer.errors

    validator = serializer.save()

    with pytest.raises(ValueError):
        validator({'count': count})



@pytest.mark.parametrize(
    'count',
    (0.1, 1, 1.1, 0),
)
def test_float_multiple_of(count):
    from flex.serializers.core import PropertiesSerializer

    schema = {
        'pk': {
            'type': NUMBER,
            'multipleOf': 0.1,
        },
    }
    serializer = PropertiesSerializer(data=schema)
    assert serializer.is_valid(), serializer.errors

    validator = serializer.save()

    validator({'pk': count})


@pytest.mark.parametrize(
    'count',
    (0.4, 1, 1.1999999999),
)
def test_float_not_multiple_of(count):
    from flex.serializers.core import PropertiesSerializer

    schema = {
        'count': {
            'type': INTEGER,
            'multipleOf': 0.3,
        },
    }
    serializer = PropertiesSerializer(data=schema)
    assert serializer.is_valid(), serializer.errors

    validator = serializer.save()

    with pytest.raises(ValueError):
        validator({'count': count})


def test_multiple_of_is_noop_if_not_required_and_not_present():
    schema = {
        'count': {
            'type': INTEGER,
            'multipleOf': 0.3,
        },
    }
    validator = generate_validator_from_schema(schema)

    validator({})

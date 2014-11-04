import pytest

from flex.constants import (
    STRING,
)

from tests.utils import generate_validator_from_schema


@pytest.mark.parametrize(
    'value,count',
    (
        ('test', 10),
        ('another-test', 15),
    )
)
def test_properties_validation_with_valid_properties(value, count):
    schema = {
        'properties': {
            'value': {'type': STRING},
            'count': {'minimum': 10, 'maximum': 15},
        },
    }

    validator = generate_validator_from_schema(schema)

    validator({
        'value': value,
        'count': count,
    })


@pytest.mark.parametrize(
    'value,count',
    (
        (5, 10),  # value should be a string
        ('another-test', 9),  # count should be at least 10
        ('test', 16),  # count should be 15 or less
    )
)
def test_properties_validation_with_invalid_values(value, count):
    schema = {
        'properties': {
            'value': {'type': STRING},
            'count': {'minimum': 10, 'maximum': 15},
        },
    }

    validator = generate_validator_from_schema(schema)

    with pytest.raises(ValueError):
        validator({
            'value': value,
            'count': count,
        })

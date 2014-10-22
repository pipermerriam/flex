import pytest

from flex.constants import (
    NUMBER,
)

from tests.utils import generate_validator_from_schema


#
# minimum and exclusiveMinimum tests
#
@pytest.mark.parametrize(
    'width',
    (5, 5.0, 6),
)
def test_inclusive_minimum_validation_with_valid_numbers(width):
    schema = {
        'width': {
            'type': NUMBER,
            'minimum': 5,
        },
    }
    validator = generate_validator_from_schema(schema)

    validator({'width': width})


@pytest.mark.parametrize(
    'width',
    (-5, 0, 4.999),
)
def test_inclusive_minimum_validation_with_invalid_numbers(width):
    schema = {
        'width': {
            'type': NUMBER,
            'minimum': 5,
        },
    }
    validator = generate_validator_from_schema(schema)

    with pytest.raises(ValueError):
        validator({'width': width})


@pytest.mark.parametrize(
    'width',
    (5.00001, 6, 10),
)
def test_exclusive_minimum_validation_with_valid_numbers(width):
    schema = {
        'width': {
            'type': NUMBER,
            'minimum': 5,
            'exclusiveMinimum': True,
        },
    }
    validator = generate_validator_from_schema(schema)

    validator({'width': width})


@pytest.mark.parametrize(
    'width',
    (5, 4.99999, 0),
)
def test_exclusive_minimum_validation_with_invalid_numbers(width):
    schema = {
        'width': {
            'type': NUMBER,
            'minimum': 5,
            'exclusiveMinimum': True,
        },
    }
    validator = generate_validator_from_schema(schema)

    with pytest.raises(ValueError):
        validator({'width': width})


#
# maximum and exclusiveMaximum tests
#
@pytest.mark.parametrize(
    'width',
    (5, 5.0, 0, -5),
)
def test_inclusive_maximum_validation_with_valid_numbers(width):
    schema = {
        'width': {
            'type': NUMBER,
            'maximum': 5,
        },
    }
    validator = generate_validator_from_schema(schema)

    validator({'width': width})


@pytest.mark.parametrize(
    'width',
    (6, 10, 5.000001),
)
def test_inclusive_maximum_validation_with_invalid_numbers(width):
    schema = {
        'width': {
            'type': NUMBER,
            'maximum': 5,
        },
    }
    validator = generate_validator_from_schema(schema)

    with pytest.raises(ValueError):
        validator({'width': width})


@pytest.mark.parametrize(
    'width',
    (4.99999, 0, -5),
)
def test_exclusive_maximum_validation_with_valid_numbers(width):
    schema = {
        'width': {
            'type': NUMBER,
            'maximum': 5,
            'exclusiveMaximum': True,
        },
    }
    validator = generate_validator_from_schema(schema)

    validator({'width': width})


@pytest.mark.parametrize(
    'width',
    (5, 5.00001, 10),
)
def test_exclusive_maximum_validation_with_invalid_numbers(width):
    schema = {
        'width': {
            'type': NUMBER,
            'maximum': 5,
            'exclusiveMaximum': True,
        },
    }
    validator = generate_validator_from_schema(schema)

    with pytest.raises(ValueError):
        validator({'width': width})
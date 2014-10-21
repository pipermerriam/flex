import pytest

from flex.constants import (
    STRING,
)

from tests.utils import generate_validator_from_schema


#
# minLength validation tests
#
@pytest.mark.parametrize(
    'zipcode',
    ('80205', '80205-1234'),
)
def test_minimum_length_with_valid_string(zipcode):
    schema = {
        'zipcode': {
            'type': STRING,
            'minLength': 5,
        },
    }
    validator = generate_validator_from_schema(schema)

    validator({'zipcode': zipcode})


@pytest.mark.parametrize(
    'zipcode',
    ('8020', 'abcd', ''),
)
def test_minimum_length_with_too_short_string(zipcode):
    schema = {
        'zipcode': {
            'type': STRING,
            'minLength': 5,
        },
    }
    validator = generate_validator_from_schema(schema)

    with pytest.raises(ValueError):
        validator({'zipcode': zipcode})


#
# maxLength validation tests
#
@pytest.mark.parametrize(
    'zipcode',
    ('80205', '1234567890', ''),
)
def test_maximum_length_with_valid_string(zipcode):
    schema = {
        'zipcode': {
            'type': STRING,
            'maxLength': 10,
        },
    }
    validator = generate_validator_from_schema(schema)

    validator({'zipcode': zipcode})


@pytest.mark.parametrize(
    'zipcode',
    ('12345-12345', 'abcde-fghijkl'),
)
def test_maximum_length_with_too_long_string(zipcode):
    schema = {
        'zipcode': {
            'type': STRING,
            'maxLength': 10,
        },
    }
    validator = generate_validator_from_schema(schema)

    with pytest.raises(ValueError):
        validator({'zipcode': zipcode})

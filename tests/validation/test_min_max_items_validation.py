import pytest

from flex.constants import (
    ARRAY,
)

from tests.utils import generate_validator_from_schema


#
# minLength validation tests
#
@pytest.mark.parametrize(
    'letters',
    (
        ['a', 'b', 'c'],
        ['a', 'b', 'c', 'd'],
    ),
)
def test_valid_array_with_min_items(letters):
    schema = {
        'letters': {
            'type': ARRAY,
            'minItems': 3,
        },
    }
    validator = generate_validator_from_schema(schema)

    validator({'letters': letters})


@pytest.mark.parametrize(
    'letters',
    (
        [],
        ['a'],
        ['a', 'b'],
    ),
)
def test_min_items_with_too_short_array(letters):
    schema = {
        'letters': {
            'type': ARRAY,
            'minItems': 3,
        },
    }
    validator = generate_validator_from_schema(schema)

    with pytest.raises(ValueError):
        validator({'letters': letters})


def test_min_items_allows_empty_when_not_required_and_not_present():
    schema = {
        'letters': {
            'type': ARRAY,
            'minItems': 3,
        },
    }
    validator = generate_validator_from_schema(schema)

    validator({})


#
# maxLength validation tests
#
@pytest.mark.parametrize(
    'letters',
    (
        [],
        ['a', 'b'],
        ['a', 'b', 'c'],
    ),
)
def test_valid_array_with_max_items(letters):
    schema = {
        'letters': {
            'type': ARRAY,
            'maxItems': 3,
        },
    }
    validator = generate_validator_from_schema(schema)

    validator({'letters': letters})


@pytest.mark.parametrize(
    'letters',
    (
        ['a', 'b', 'c', 'd'],
        ['a', 'b', 'c', 'd', 'e'],
    ),
)
def test_max_items_with_too_long_array(letters):
    schema = {
        'letters': {
            'type': ARRAY,
            'maxItems': 3,
        },
    }
    validator = generate_validator_from_schema(schema)

    with pytest.raises(ValueError):
        validator({'letters': letters})


def test_max_items_allows_empty_when_not_required_and_not_present():
    schema = {
        'letters': {
            'type': ARRAY,
            'maxItems': 3,
        },
    }
    validator = generate_validator_from_schema(schema)

    validator({})

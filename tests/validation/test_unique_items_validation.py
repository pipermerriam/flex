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
        [],
        ['a', 'b', 'c'],
        ['a', 'b', 'c', 'd'],
    ),
)
def test_unique_items_with_unique_array(letters):
    schema = {
        'letters': {
            'type': ARRAY,
            'uniqueItems': True,
        },
    }
    validator = generate_validator_from_schema(schema)

    validator({'letters': letters})


@pytest.mark.parametrize(
    'letters',
    (
        ['a', 'b', 'a'],
        [1, 2, 3, 1],
        [True, True],
    ),
)
def test_unique_items_with_dupes_in_array(letters):
    schema = {
        'letters': {
            'type': ARRAY,
            'uniqueItems': True,
        },
    }
    validator = generate_validator_from_schema(schema)

    with pytest.raises(ValueError):
        validator({'letters': letters})


def test_unique_items_is_noop_when_not_required_and_not_present():
    schema = {
        'letters': {
            'type': ARRAY,
            'uniqueItems': True,
        },
    }
    validator = generate_validator_from_schema(schema)

    validator({})

import pytest

from flex.constants import EMPTY

from tests.utils import generate_validator_from_schema


#
# minLength validation tests
#
@pytest.mark.parametrize(
    'letters',
    ('a', 'b', True, 1, 2),
)
def test_enum_with_valid_array(letters):
    schema = {
        'enum': [2, 1, 'a', 'b', 'c', True, False],
    }
    validator = generate_validator_from_schema(schema)

    validator(letters)


@pytest.mark.parametrize(
    'letters',
    (None, 1, 0, 2, 'a'),
)
def test_enum_with_invalid_items(letters):
    schema = {
        'enum': [True, False, 1.0, 2.0, 'A'],
    }
    validator = generate_validator_from_schema(schema)

    with pytest.raises(ValueError):
        validator(letters)


def test_enum_noop_when_not_required_and_field_not_present():
    schema = {
        'enum': [True, False, 1.0, 2.0, 'A'],
    }
    validator = generate_validator_from_schema(schema)

    validator(EMPTY)

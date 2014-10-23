import pytest

from flex.constants import (
    OBJECT,
    EMPTY,
)

from tests.utils import generate_validator_from_schema


#
# minLength validation tests
#
@pytest.mark.parametrize(
    'element',
    (
        {'id': 1},
        {},
    ),
)
def test_min_properties_with_too_few_properties(element):
    schema = {
        'type': OBJECT,
        'minProperties': 2,
    }
    validator = generate_validator_from_schema(schema)

    with pytest.raises(ValueError):
        validator(element)


@pytest.mark.parametrize(
    'element',
    (
        {'id': 1, 'class': 'foo'},
        {'id': 2, 'class': 'bar', 'targets': []},
    ),
)
def test_min_properties_with_enough_properties(element):
    schema = {
        'type': OBJECT,
        'minProperties': 2,
    }
    validator = generate_validator_from_schema(schema)

    validator(element)


def test_min_properties_is_noop_when_not_required_or_present():
    schema = {
        'type': OBJECT,
        'minProperties': 2,
    }
    validator = generate_validator_from_schema(schema)

    validator(EMPTY)


#
# maxLength validation tests
#
@pytest.mark.parametrize(
    'element',
    (
        {'id': 1, 'class': 'foo', 'targets': []},
        {'id': 2, 'class': 'bar', 'targets': [], 'baz': 3},
    ),
)
def test_max_properties_with_too_many_properties(element):
    schema = {
        'type': OBJECT,
        'maxProperties': 2,
    }
    validator = generate_validator_from_schema(schema)

    with pytest.raises(ValueError):
        validator(element)


@pytest.mark.parametrize(
    'element',
    (
        {},
        {'id': 1},
        {'id': 1, 'class': 'foo'},
    ),
)
def test_max_properties_with_enough_properties(element):
    schema = {
        'type': OBJECT,
        'maxProperties': 2,
    }
    validator = generate_validator_from_schema(schema)

    validator(element)


def test_max_properties_is_noop_when_not_required_or_present():
    schema = {
        'type': OBJECT,
        'maxProperties': 2,
    }
    validator = generate_validator_from_schema(schema)

    validator(EMPTY)

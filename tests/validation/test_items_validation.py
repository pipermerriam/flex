import pytest

from flex.constants import (
    ARRAY,
    INTEGER,
    STRING,
)

from tests.utils import generate_validator_from_schema


@pytest.mark.parametrize(
    'items',
    (
        [1, 2, 3, 4, -1, -2, 8, 9],  # -1 and -2 are less than minimum
        [1, 2, 3, 4, 15, 16, 5, 6, 7],  # 15 and 16 are greater than maximum
        [1, 2, 3, '4', '5', 6],  # string not allowed.
    )
)
def test_invalid_values_against_single_schema(items):
    from django.core.exceptions import ValidationError

    schema = {
        'type': ARRAY,
        'items': {
            'type': INTEGER,
            'minimum': 0,
            'maximum': 10,
        }
    }

    validator = generate_validator_from_schema(schema)

    with pytest.raises(ValidationError) as err:
        validator(items, inner=True)

    assert 'items' in err.value.messages[0]
    assert len(err.value.messages[0]['items']) == 2


@pytest.mark.parametrize(
    'items',
    (
        [1, 2, 3, 4, -1, -2, 8, 9],  # -1 and -2 are less than minimum
        [1, 2, 3, 4, 15, 16, 5, 6, 7],  # 15 and 16 are greater than maximum
        [1, 2, 3, '4', '5', 6],  # string not allowed.
    )
)
def test_invalid_values_against_schema_reference(items):
    from django.core.exceptions import ValidationError

    schema = {
        'type': ARRAY,
        'items': 'SomeReference',
    }
    context = {
        'definitions': {
            'SomeReference': {
                'type': INTEGER,
                'minimum': 0,
                'maximum': 10,
            },
        },
    }

    validator = generate_validator_from_schema(schema, context=context)

    with pytest.raises(ValidationError) as err:
        validator(items, inner=True)

    assert 'items' in err.value.messages[0]
    assert len(err.value.messages[0]['items']) == 2


def test_invalid_values_against_list_of_schemas():
    from django.core.exceptions import ValidationError

    schema = {
        'type': ARRAY,
        'items': [
            {'type': INTEGER, 'minimum': 0, 'maximum': 10},
            {'type': STRING, 'minLength': 3, 'maxLength': 5},
            {'type': INTEGER, 'minimum': 0, 'maximum': 10},
            {'type': STRING, 'minLength': 3, 'maxLength': 5},
            {'type': INTEGER, 'minimum': 0, 'maximum': 10},
        ],
    }

    validator = generate_validator_from_schema(schema)

    with pytest.raises(ValidationError) as err:
        validator(
            [11, 'abc-abc', -5, 'ab', 'wrong-type'],
            inner=True,
        )

    assert 'items' in err.value.messages[0]
    assert len(err.value.messages[0]['items']) == 5
    _1, _2, _3, _4, _5 = err.value.messages[0]['items']

    assert 'maximum' in _1
    assert 'maxLength' in _2
    assert 'minimum' in _3
    assert 'minLength' in _4
    assert 'type' in _5


def test_items_past_the_number_of_schemas_provided_are_skipped():
    from django.core.exceptions import ValidationError

    schema = {
        'type': ARRAY,
        'items': [
            {'type': INTEGER, 'minimum': 0, 'maximum': 10},
            {'type': INTEGER, 'minimum': 0, 'maximum': 10},
            {'type': INTEGER, 'minimum': 0, 'maximum': 10},
        ],
    }

    validator = generate_validator_from_schema(schema)

    validator(
        [0, 5, 10, 20, 30, 40],
        # 20, 30, and 40 don't conform, but are beyond the declared number of schemas.
        inner=True,
    )

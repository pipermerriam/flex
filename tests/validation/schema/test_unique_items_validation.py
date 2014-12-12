import pytest

from flex.exceptions import (
    ValidationError,
)
from flex.error_messages import (
    MESSAGES,
)
from flex.constants import (
    ARRAY,
    EMPTY,
)

from tests.utils import (
    generate_validator_from_schema,
    assert_error_message_equal,
)


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
        'type': ARRAY,
        'uniqueItems': True,
    }
    validator = generate_validator_from_schema(schema)

    validator(letters)


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
        'type': ARRAY,
        'uniqueItems': True,
    }
    validator = generate_validator_from_schema(schema)

    with pytest.raises(ValidationError) as err:
        validator(letters)

    assert 'uniqueItems' in err.value.messages[0]
    assert_error_message_equal(
        err.value.messages[0]['uniqueItems'][0],
        MESSAGES['unique_items']['invalid'],
    )


def test_unique_items_is_noop_when_not_required_and_not_present():
    schema = {
        'type': ARRAY,
        'uniqueItems': True,
    }
    validator = generate_validator_from_schema(schema)

    validator(EMPTY)

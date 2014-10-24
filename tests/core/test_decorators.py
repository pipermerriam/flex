import pytest

from flex.decorators import skip_if_not_of_type
from flex.constants import (
    NUMBER,
    EMPTY,
)


@pytest.mark.parametrize(
    'v',
    (0, 1, 2, -2, 0.0, 1.0, 2.0, -2.0),
)
def test_type_enforcement_accepts_valid_types(v):
    @skip_if_not_of_type(NUMBER)
    def fn(value):
        return True

    assert fn(v) is True


@pytest.mark.parametrize(
    'v',
    (True, False, '', None, [], {}, 'abcd', ['a'], {'a': 1}),
)
def test_type_enforcement_detects_invalid_types(v):
    @skip_if_not_of_type(NUMBER)
    def fn(value):
        raise Exception('should not happen')

    fn(v)

import pytest

from flex.decorators import enforce_type
from flex.constants import (
    NUMBER,
    EMPTY,
)


@pytest.mark.parametrize(
    'v',
    (0, 1, 2, -2, 0.0, 1.0, 2.0, -2.0),
)
def test_type_enforcement_accepts_valid_types(v):
    @enforce_type(NUMBER)
    def fn(value):
        pass

    fn(v)


@pytest.mark.parametrize(
    'v',
    (True, False, '', None, [], {}, 'abcd', ['a'], {'a': 1}),
)
def test_type_enforcement_detects_invalid_types(v):
    from rest_framework import serializers

    @enforce_type(NUMBER)
    def fn(value):
        pass

    with pytest.raises(serializers.ValidationError):
        fn(v)


def test_type_enforcement_skips_empty_value():
    from rest_framework import serializers

    @enforce_type(NUMBER)
    def fn(value):
        pass

    fn(EMPTY)

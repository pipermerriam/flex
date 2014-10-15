import pytest

from flex.serializers.core import (
    HeaderSerializer,
)
from flex.constants import (
    BOOLEAN,
    NUMBER,
    ARRAY,
    STRING,
)

from tests.utils import assert_error_message_equal


def test_items_is_required_when_type_is_array():
    serializer = HeaderSerializer(
        data={'type': ARRAY},
    )

    assert not serializer.is_valid()
    assert 'items' in serializer.errors
    assert_error_message_equal(
        serializer.errors['items'][0],
        serializer.error_messages['items_required'],
    )


@pytest.mark.parametrize(
    'type_,default',
    (
        (BOOLEAN, 'abc'),
        (BOOLEAN, 1),
        (NUMBER, True),
        (NUMBER, 'abc'),
        (ARRAY, 'abc'),
        (STRING, 1),
        (STRING, None),
    )
)
def test_mistyped_header_default_boolean_to_string(type_, default):
    serializer = HeaderSerializer(
        data={'type': type_, 'default': default}
    )

    assert not serializer.is_valid()
    assert 'default' in serializer.errors
    assert_error_message_equal(
        serializer.errors['default'][0],
        serializer.error_messages['default_is_incorrect_type'],
    )

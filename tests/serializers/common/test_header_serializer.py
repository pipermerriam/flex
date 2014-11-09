from flex.serializers.core import (
    HeaderSerializer,
)
from flex.constants import (
    OBJECT,
)
from flex.error_messages import MESSAGES

from tests.utils import assert_error_message_equal


def test_header_type_cannot_be_object():
    serializer = HeaderSerializer(
        data={'type': OBJECT},
    )

    assert not serializer.is_valid()
    assert 'type' in serializer.errors
    assert_error_message_equal(
        serializer.errors['type'][0],
        MESSAGES['type']['invalid_header_type'],
    )

from flex.serializers.core import ParameterSerializer
from flex.error_messages import MESSAGES

from tests.utils import assert_error_message_equal


def test_unknown_parameter_reference():
    serializer = ParameterSerializer(
        data=['SomeReference'],
        context={},
        many=True,
    )

    assert not serializer.is_valid()
    assert_error_message_equal(
        serializer.errors[0][0],
        MESSAGES['unknown_reference']['parameter'],
    )


def test_valid_parameter_reference():
    serializer = ParameterSerializer(
        data=['SomeReference'],
        context={
            'parameters': {'SomeReference': {}},
        },
        many=True,
    )

    assert serializer.is_valid()

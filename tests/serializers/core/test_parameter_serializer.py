from flex.serializers.core import ParameterSerializer

from tests.utils import assert_error_message_equal


def test_unknown_parameter_reference():
    serializer = ParameterSerializer(
        data=['SomeReference'],
        context={},
    )

    assert not serializer.is_valid()
    assert 'non_field_errors' in serializer.errors[0]
    assert_error_message_equal(
        serializer.errors[0]['non_field_errors'][0],
        serializer.error_messages['unknown_reference']
    )


def test_valid_parameter_reference():
    serializer = ParameterSerializer(
        data=['SomeReference'],
        context={
            'parameters': {'SomeReference': {}},
        },
    )

    assert serializer.is_valid()

import pytest

from flex.serializers.core import ParameterSerializer
from flex.validation.parameter import (
    validate_parameters,
)
from flex.constants import (
    PATH,
    INTEGER,
    NUMBER,
    STRING,
    UUID,
    DATETIME,
)
from flex.error_messages import MESSAGES

from tests.utils import assert_error_message_equal


@pytest.mark.parametrize(
    'format_,value,error_key',
    (
        (UUID, 'not-a-real-uuid', 'invalid_uuid'),
        (DATETIME, '2011-13-18T10:29:47+03:00', 'invalid_datetime'),  # Invalid month 13
    )
)
def test_parameter_format_validation_on_invalid_values(format_, value, error_key):
    from django.core.exceptions import ValidationError
    serializer = ParameterSerializer(many=True, data=(
        {
            'name': 'id',
            'in': PATH,
            'description': 'id',
            'type': STRING,
            'required': True,
            'format': format_,
        },
    ))
    assert serializer.is_valid(), serializer.errors
    parameters = serializer.object
    parameter_values = {
        'id': value,
    }

    with pytest.raises(ValidationError) as err:
        validate_parameters(parameter_values, parameters, {}, inner=True)

    assert 'id' in err.value.messages[0]
    assert 'format' in err.value.messages[0]['id'][0]
    assert_error_message_equal(
        err.value.messages[0]['id'][0]['format'][0],
        MESSAGES['format'][error_key],
    )


@pytest.mark.parametrize(
    'format_,value',
    (
        (UUID, '536aa369-5b29-4367-b5a4-2696565f4e8a'),
        (DATETIME, '2011-12-18T10:29:47+03:00'),
    ),
)
def test_parameter_format_validation_succeeds_on_valid_values(format_, value):
    serializer = ParameterSerializer(many=True, data=(
        {
            'name': 'id',
            'in': PATH,
            'description': 'id',
            'type': STRING,
            'required': True,
            'format': format_,
        },
    ))
    assert serializer.is_valid(), serializer.errors
    parameters = serializer.object
    parameter_values = {
        'id': value,
    }

    validate_parameters(parameter_values, parameters, {})

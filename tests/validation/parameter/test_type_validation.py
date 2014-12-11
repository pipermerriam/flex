import pytest

from flex.exceptions import ValidationError
from flex.serializers.core import ParameterSerializer
from flex.validation.parameter import (
    validate_parameters,
)
from flex.constants import (
    PATH,
    INTEGER,
    NUMBER,
    STRING,
)
from flex.error_messages import MESSAGES

from tests.utils import assert_error_message_equal


@pytest.mark.parametrize(
    'type_,value',
    (
        (INTEGER, 1.0),
        (INTEGER, '1234'),
        (NUMBER, '1234'),
        (STRING, 1234),
    ),
)
def test_parameter_validation_enforces_type(type_, value):
    serializer = ParameterSerializer(many=True, data=(
        {'name': 'id', 'in': PATH, 'description': 'id', 'type': type_, 'required': True},
    ))
    assert serializer.is_valid(), serializer.errors
    parameters = serializer.object
    parameter_values = {
        'id': value,
    }

    with pytest.raises(ValidationError) as err:
        validate_parameters(parameter_values, parameters, {}, inner=True)

    assert 'id' in err.value.messages[0]
    assert 'type' in err.value.messages[0]['id'][0]
    assert_error_message_equal(
        err.value.messages[0]['id'][0]['type'][0],
        MESSAGES['type']['invalid'],
    )


@pytest.mark.parametrize(
    'type_,value',
    (
        (INTEGER, 1),
        (INTEGER, 0),
        (INTEGER, 1234),
        (NUMBER, 1),
        (NUMBER, 0),
        (NUMBER, 1234),
        (NUMBER, 1.5),
        (NUMBER, 0.5),
        (NUMBER, 12.34),
        (STRING, '1234'),
        (STRING, 'abcd'),
    ),
)
def test_parameter_validation_with_correct_type(type_, value):
    serializer = ParameterSerializer(many=True, data=(
        {'name': 'id', 'in': PATH, 'description': 'id', 'type': type_, 'required': True},
    ))
    assert serializer.is_valid(), serializer.errors
    parameters = serializer.object
    parameter_values = {
        'id': value,
    }

    validate_parameters(parameter_values, parameters, {}, inner=True)

import pytest

from flex.serializers.core import ParameterSerializer
from flex.validation.parameter import (
    validate_parameters,
)
from flex.constants import (
    PATH,
    NUMBER,
)
from flex.error_messages import MESSAGES

from tests.utils import assert_error_message_equal


@pytest.mark.parametrize(
    'divisor,value',
    (
        (3, 4),
        (2, 1),
        (0.19, 1.2),
        (7, 15),
    ),
)
def test_multiple_of_validation_for_invalid_values(divisor, value):
    from django.core.exceptions import ValidationError
    serializer = ParameterSerializer(many=True, data=(
        {
            'name': 'id',
            'in': PATH,
            'description':'id',
            'type': NUMBER,
            'required': True,
            'multipleOf': divisor,
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
    assert 'multipleOf' in err.value.messages[0]['id'][0]
    assert_error_message_equal(
        err.value.messages[0]['id'][0]['multipleOf'][0],
        MESSAGES['multiple_of']['invalid'],
    )


@pytest.mark.parametrize(
    'divisor,value',
    (
        (0.2, 1),
        (2, 10),
        (0.1, 10),
    ),
)
def test_multiple_of_validation_for_valid_multiples(divisor, value):
    serializer = ParameterSerializer(many=True, data=(
        {
            'name': 'id',
            'in': PATH,
            'description':'id',
            'type': NUMBER,
            'required': True,
            'multipleOf': divisor,
        },
    ))
    assert serializer.is_valid(), serializer.errors
    parameters = serializer.object
    parameter_values = {
        'id': value,
    }

    validate_parameters(parameter_values, parameters, {}, inner=True)

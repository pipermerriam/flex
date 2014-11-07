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


#
# minimum validation tests
#
@pytest.mark.parametrize(
    'minimum,value',
    (
        (0, -1),
        (-5, -6),
        (10, 9.999),
    ),
)
def test_minimum_validation_for_invalid_values(minimum, value):
    from django.core.exceptions import ValidationError
    serializer = ParameterSerializer(many=True, data=(
        {
            'name': 'id',
            'in': PATH,
            'description':'id',
            'type': NUMBER,
            'required': True,
            'minimum': minimum,
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
    assert 'minimum' in err.value.messages[0]['id'][0]
    assert_error_message_equal(
        err.value.messages[0]['id'][0]['minimum'][0],
        MESSAGES['minimum']['invalid'],
    )


@pytest.mark.parametrize(
    'minimum,value',
    (
        (0, -1),
        (0, 0),
        (-5, -6),
        (-5, -5),
        (10, 9.999),
        (10, 10),
    ),
)
def test_exclusive_minimum_validation_for_invalid_values(minimum, value):
    from django.core.exceptions import ValidationError
    serializer = ParameterSerializer(many=True, data=(
        {
            'name': 'id',
            'in': PATH,
            'description':'id',
            'type': NUMBER,
            'required': True,
            'minimum': minimum,
            'exclusiveMinimum': True,
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
    assert 'minimum' in err.value.messages[0]['id'][0]
    assert_error_message_equal(
        err.value.messages[0]['id'][0]['minimum'][0],
        MESSAGES['minimum']['invalid'],
    )


@pytest.mark.parametrize(
    'minimum,value',
    (
        (0, 0),
        (0, 1),
        (-5, -5),
        (-5, 5),
        (10, 15),
    ),
)
def test_minimum_validation_for_valid_values(minimum, value):
    serializer = ParameterSerializer(many=True, data=(
        {
            'name': 'id',
            'in': PATH,
            'description':'id',
            'type': NUMBER,
            'required': True,
            'minimum': minimum,
        },
    ))
    assert serializer.is_valid(), serializer.errors
    parameters = serializer.object
    parameter_values = {
        'id': value,
    }

    validate_parameters(parameter_values, parameters, {}, inner=True)


@pytest.mark.parametrize(
    'minimum,value',
    (
        (-1, 1),
        (0, 0.00001),
        (10, 10.0001),
    ),
)
def test_exclusive_minimum_validation_for_valid_values(minimum, value):
    serializer = ParameterSerializer(many=True, data=(
        {
            'name': 'id',
            'in': PATH,
            'description':'id',
            'type': NUMBER,
            'required': True,
            'minimum': minimum,
            'exclusiveMinimum': True,
        },
    ))
    assert serializer.is_valid(), serializer.errors
    parameters = serializer.object
    parameter_values = {
        'id': value,
    }

    validate_parameters(parameter_values, parameters, {}, inner=True)


#
# maximum validation tests
#
@pytest.mark.parametrize(
    'maximum,value',
    (
        (5, 6),
        (-5, -4),
        (10, 10.0001),
    ),
)
def test_maximum_validation_for_invalid_values(maximum, value):
    from django.core.exceptions import ValidationError
    serializer = ParameterSerializer(many=True, data=(
        {
            'name': 'id',
            'in': PATH,
            'description':'id',
            'type': NUMBER,
            'required': True,
            'maximum': maximum,
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
    assert 'maximum' in err.value.messages[0]['id'][0]
    assert_error_message_equal(
        err.value.messages[0]['id'][0]['maximum'][0],
        MESSAGES['maximum']['invalid'],
    )


@pytest.mark.parametrize(
    'maximum,value',
    (
        (5, 6),
        (5, 5),
        (-5, -4),
        (-5, -5),
        (10, 10.0001),
        (10, 10),
    ),
)
def test_exclusive_maximum_validation_for_invalid_values(maximum, value):
    from django.core.exceptions import ValidationError
    serializer = ParameterSerializer(many=True, data=(
        {
            'name': 'id',
            'in': PATH,
            'description':'id',
            'type': NUMBER,
            'required': True,
            'maximum': maximum,
            'exclusiveMaximum': True,
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
    assert 'maximum' in err.value.messages[0]['id'][0]
    assert_error_message_equal(
        err.value.messages[0]['id'][0]['maximum'][0],
        MESSAGES['maximum']['invalid'],
    )


@pytest.mark.parametrize(
    'maximum,value',
    (
        (0, 0),
        (1, 0),
        (-5, -5),
        (-5, -6),
        (10, 9),
    ),
)
def test_maximum_validation_for_valid_values(maximum, value):
    serializer = ParameterSerializer(many=True, data=(
        {
            'name': 'id',
            'in': PATH,
            'description':'id',
            'type': NUMBER,
            'required': True,
            'maximum': maximum,
        },
    ))
    assert serializer.is_valid(), serializer.errors
    parameters = serializer.object
    parameter_values = {
        'id': value,
    }

    validate_parameters(parameter_values, parameters, {}, inner=True)


@pytest.mark.parametrize(
    'maximum,value',
    (
        (-1, -1.00001),
        (0, -0.000001),
        (10, 9),
    ),
)
def test_exclusive_maximum_validation_for_valid_values(maximum, value):
    serializer = ParameterSerializer(many=True, data=(
        {
            'name': 'id',
            'in': PATH,
            'description':'id',
            'type': NUMBER,
            'required': True,
            'maximum': maximum,
            'exclusiveMaximum': True,
        },
    ))
    assert serializer.is_valid(), serializer.errors
    parameters = serializer.object
    parameter_values = {
        'id': value,
    }

    validate_parameters(parameter_values, parameters, {}, inner=True)

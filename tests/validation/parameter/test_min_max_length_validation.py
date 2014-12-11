import pytest

from flex.exceptions import ValidationError
from flex.serializers.core import ParameterSerializer
from flex.validation.parameter import (
    validate_parameters,
)
from flex.constants import (
    PATH,
    STRING,
)


#
# minimum validation tests
#
@pytest.mark.parametrize(
    'min_length,value',
    (
        (1, ''),
        (2, 'a'),
        (5, '1234'),
    ),
)
def test_minimum_length_validation_with_too_short_values(min_length, value):
    serializer = ParameterSerializer(many=True, data=(
        {
            'name': 'id',
            'in': PATH,
            'description':'id',
            'type': STRING,
            'required': True,
            'minLength': min_length,
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
    assert 'minLength' in err.value.messages[0]['id'][0]



@pytest.mark.parametrize(
    'min_length,value',
    (
        (1, 'a'),
        (2, 'ab'),
        (2, '12345'),
        (5, '12345-abcde'),
    ),
)
def test_minimum_length_validation_with_valid_lengths(min_length, value):
    serializer = ParameterSerializer(many=True, data=(
        {
            'name': 'id',
            'in': PATH,
            'description':'id',
            'type': STRING,
            'required': True,
            'minLength': min_length,
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
    'max_length,value',
    (
        (1, 'ab'),
        (5, '123456'),
    ),
)
def test_maximum_length_validation_with_too_long_values(max_length, value):
    serializer = ParameterSerializer(many=True, data=(
        {
            'name': 'id',
            'in': PATH,
            'description':'id',
            'type': STRING,
            'required': True,
            'maxLength': max_length,
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
    assert 'maxLength' in err.value.messages[0]['id'][0]



@pytest.mark.parametrize(
    'max_length,value',
    (
        (1, 'a'),
        (2, 'ab'),
        (2, '12'),
        (5, '12345'),
    ),
)
def test_maximum_length_validation_with_valid_lengths(max_length, value):
    serializer = ParameterSerializer(many=True, data=(
        {
            'name': 'id',
            'in': PATH,
            'description':'id',
            'type': STRING,
            'required': True,
            'maxLength': max_length,
        },
    ))
    assert serializer.is_valid(), serializer.errors
    parameters = serializer.object
    parameter_values = {
        'id': value,
    }

    validate_parameters(parameter_values, parameters, {}, inner=True)

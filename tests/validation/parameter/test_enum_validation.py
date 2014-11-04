import pytest

from flex.serializers.core import ParameterSerializer
from flex.validation.parameter import (
    validate_parameters,
)
from flex.constants import (
    PATH,
    STRING,
    NUMBER,
    BOOLEAN,
)
from flex.error_messages import MESSAGES

from tests.utils import assert_error_message_equal


#
# enum validation tests
#
@pytest.mark.parametrize(
    'enum,value',
    (
        ([True, False], 0),
        ([True, False], 1),
        ([True, False], ''),
        ([0, 1, 2, 3], True),
        ([0, 1, 2, 3], False),
        ([0, 1, 2, 3], '1'),
        ([0, 1, 2, 3], 4),
        ([0, 1, 2, 3], 1.0),
        (['1', '2', 'a', 'b'], 'A'),
        (['1', '2', 'a', 'b'], 1),
        (['1', '2', 'a', 'b'], 2),
    ),
)
def test_enum_validation_with_invalid_values(enum, value):
    from django.core.exceptions import ValidationError
    serializer = ParameterSerializer(many=True, data=(
        {
            'name': 'id',
            'in': PATH,
            'description':'id',
            'type': [STRING, NUMBER, BOOLEAN],
            'required': True,
            'enum': enum,
        },
    ))
    assert serializer.is_valid(), serializer.errors
    parameters = serializer.object
    parameter_values = {
        'id': value,
    }

    with pytest.raises(ValidationError) as err:
        validate_parameters(parameter_values, parameters, inner=True)

    assert 'id' in err.value.messages[0]
    assert 'enum' in err.value.messages[0]['id'][0]
    assert_error_message_equal(
        err.value.messages[0]['id'][0]['enum'][0],
        MESSAGES['enum']['invalid'],
    )



@pytest.mark.parametrize(
    'enum,value',
    (
        ([True, False], True),
        ([True, False], False),
        ([0, 1, 2, 3], 3),
        ([0, 1, 2, 3], 1),
        (['1', '2', 'a', 'b'], 'a'),
        (['1', '2', 'a', 'b'], '1'),
    ),
)
def test_enum_validation_with_allowed_values(enum, value):
    serializer = ParameterSerializer(many=True, data=(
        {
            'name': 'id',
            'in': PATH,
            'description':'id',
            'type': [STRING, NUMBER, BOOLEAN],
            'required': True,
            'enum': enum,
        },
    ))
    assert serializer.is_valid(), serializer.errors
    parameters = serializer.object
    parameter_values = {
        'id': value,
    }

    validate_parameters(parameter_values, parameters, inner=True)

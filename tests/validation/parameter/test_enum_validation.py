import pytest

from flex.exceptions import ValidationError
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

from tests.utils import assert_message_in_errors


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
    serializer = ParameterSerializer(many=True, data=[
        {
            'name': 'id',
            'in': PATH,
            'description':'id',
            'type': [STRING, NUMBER, BOOLEAN],
            'required': True,
            'enum': enum,
        },
    ])
    assert serializer.is_valid(), serializer.errors
    parameters = serializer.save()
    parameter_values = {
        'id': value,
    }

    with pytest.raises(ValidationError) as err:
        validate_parameters(parameter_values, parameters, {})

    assert_message_in_errors(
        MESSAGES['enum']['invalid'],
        err.value.detail,
        'id.enum',
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
    serializer = ParameterSerializer(many=True, data=[
        {
            'name': 'id',
            'in': PATH,
            'description':'id',
            'type': [STRING, NUMBER, BOOLEAN],
            'required': True,
            'enum': enum,
        },
    ])
    assert serializer.is_valid(), serializer.errors
    parameters = serializer.save()
    parameter_values = {
        'id': value,
    }

    validate_parameters(parameter_values, parameters, {})

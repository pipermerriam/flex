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
from flex.error_messages import MESSAGES

from tests.utils import assert_error_message_equal


#
# pattern validation tests
#
@pytest.mark.parametrize(
    'pattern,value',
    (
        ("(?P<id>[0-9]+)", 'abcd'),  # Non digit in group
        ("[0-9]+", 'abcd'),  # Non digit not in group
    ),
)
def test_pattern_validation_with_invalid_values(pattern, value):
    serializer = ParameterSerializer(many=True, data=[
        {
            'name': 'id',
            'in': PATH,
            'description':'id',
            'type': STRING,
            'required': True,
            'pattern': pattern,
        },
    ])
    assert serializer.is_valid(), serializer.errors
    parameters = serializer.save()
    parameter_values = {
        'id': value,
    }

    with pytest.raises(ValidationError) as err:
        validate_parameters(parameter_values, parameters, {}, inner=True)

    assert 'id' in err.value.messages[0]
    assert 'pattern' in err.value.messages[0]['id'][0]
    assert_error_message_equal(
        err.value.messages[0]['id'][0]['pattern'][0],
        MESSAGES['pattern']['invalid'],
    )


@pytest.mark.parametrize(
    'pattern,value',
    (
        ("(?P<id>[0-9]+)", '1234'),  # Non digit in group
        ("[0-9]+", '1234'),  # Non digit not in group
    ),
)
def test_pattern_validation_with_matching_values(pattern, value):
    serializer = ParameterSerializer(many=True, data=[
        {
            'name': 'id',
            'in': PATH,
            'description':'id',
            'type': STRING,
            'required': True,
            'pattern': pattern,
        },
    ])
    assert serializer.is_valid(), serializer.errors
    parameters = serializer.save()
    parameter_values = {
        'id': value,
    }

    validate_parameters(parameter_values, parameters, {}, inner=True)

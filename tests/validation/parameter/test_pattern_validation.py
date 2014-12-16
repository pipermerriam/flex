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

from tests.utils import assert_message_in_errors


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
        validate_parameters(parameter_values, parameters, {})

    assert_message_in_errors(
        MESSAGES['pattern']['invalid'],
        err.value.detail,
        'id.pattern',
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

    validate_parameters(parameter_values, parameters, {})

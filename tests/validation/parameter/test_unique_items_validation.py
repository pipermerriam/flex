import pytest

from flex.exceptions import ValidationError
from flex.serializers.core import ParameterSerializer
from flex.validation.parameter import (
    validate_parameters,
)
from flex.constants import (
    PATH,
    ARRAY,
    STRING,
    NUMBER,
    BOOLEAN,
)
from flex.error_messages import MESSAGES

from tests.utils import assert_message_in_errors


#
# unique_items validation tests
#
@pytest.mark.parametrize(
    'value',
    (
        [1, 2, 3, 1],
        ['a', 'b', 'c', 'z', 'c'],
        [True, False, True],
    ),
)
def test_unique_items_validation_with_duplicates(value):
    serializer = ParameterSerializer(many=True, data=[
        {
            'name': 'id',
            'in': PATH,
            'description':'id',
            'type': ARRAY,
            'required': True,
            'uniqueItems': True,
            'items': {'type': [STRING, NUMBER, BOOLEAN]},
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
        MESSAGES['unique_items']['invalid'],
        err.value.detail,
        'id.uniqueItems',
    )


@pytest.mark.parametrize(
    'value',
    (
        [True, 1, '1'],
        [False, 0, ''],
        ['1', 1],
        ['a', 'b', 'A', 'B'],
    ),
)
def test_unique_items_validation_with_no_duplicates(value):
    serializer = ParameterSerializer(many=True, data=[
        {
            'name': 'id',
            'in': PATH,
            'description':'id',
            'type': ARRAY,
            'required': True,
            'uniqueItems': True,
            'items': {'type': [STRING, NUMBER, BOOLEAN]},
        },
    ])
    assert serializer.is_valid(), serializer.errors
    parameters = serializer.save()
    parameter_values = {
        'id': value,
    }

    validate_parameters(parameter_values, parameters, {})

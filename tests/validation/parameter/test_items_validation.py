import pytest

from flex.exceptions import ValidationError
from flex.serializers.core import ParameterSerializer
from flex.validation.parameter import (
    validate_parameters,
)
from flex.constants import (
    QUERY,
    INTEGER,
    ARRAY,
)
from flex.error_messages import MESSAGES

from tests.utils import assert_message_in_errors


def test_parameter_items_validation_on_invalid_array():
    serializer = ParameterSerializer(many=True, data=[
        {
            'name': 'id',
            'in': QUERY,
            'description': 'id',
            'items': {
                'type': INTEGER,
                'minimum': 0,
            },
            'type': ARRAY,
        },
    ])
    assert serializer.is_valid(), serializer.errors
    parameters = serializer.save()
    value = [1, 2, '3', -1, 4]
    parameter_values = {
        'id': value,
    }

    with pytest.raises(ValidationError) as err:
        validate_parameters(parameter_values, parameters, context={})

    assert_message_in_errors(
        MESSAGES['minimum']['invalid'],
        err.value.detail,
        'id.items.type',
    )
    assert_message_in_errors(
        MESSAGES['minimum']['invalid'],
        err.value.detail,
        'id.items.minimum',
    )


def test_parameter_items_validation_on_valid_value():
    serializer = ParameterSerializer(many=True, data=[
        {
            'name': 'id',
            'in': QUERY,
            'description': 'id',
            'items': {
                'type': INTEGER,
                'minimum': 0,
            },
            'type': ARRAY,
        },
    ])
    assert serializer.is_valid(), serializer.errors
    parameters = serializer.save()
    value = [1, 2, 3, 4, 5]
    parameter_values = {
        'id': value,
    }

    validate_parameters(parameter_values, parameters, context={})

import pytest

from flex.exceptions import ValidationError
from flex.serializers.core import ParameterSerializer
from flex.validation.parameter import (
    validate_parameters,
)
from flex.constants import (
    PATH,
    BODY,
    STRING,
)
from flex.error_messages import MESSAGES

from tests.utils import assert_message_in_errors


def test_required_parameters_invalid_when_not_present():
    serializer = ParameterSerializer(many=True, data=[
        {'name': 'id', 'in': PATH, 'description': 'id', 'type': STRING, 'required': True},
    ])
    assert serializer.is_valid(), serializer.errors
    parameters = serializer.save()
    parameter_values = {}

    with pytest.raises(ValidationError) as err:
        validate_parameters(parameter_values, parameters, {})

    assert_message_in_errors(
        MESSAGES['required']['required'],
        err.value.detail,
        'id.required',
    )


def test_parameters_allowed_missing_when_not_required():
    serializer = ParameterSerializer(many=True, data=[
        {
            'name': 'id',
            'in': BODY,
            'description': 'id',
            'type': STRING,
            'required': False,
            'schema': {
                'type': STRING,
            },
        },
    ])
    assert serializer.is_valid(), serializer.errors
    parameters = serializer.save()
    parameter_values = {}

    validate_parameters(parameter_values, parameters, {})

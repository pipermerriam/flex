import pytest

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

from tests.utils import assert_error_message_equal


def test_required_parameters_invalid_when_not_present():
    from django.core.exceptions import ValidationError
    serializer = ParameterSerializer(many=True, data=(
        {'name': 'id', 'in': PATH, 'description': 'id', 'type': STRING, 'required': True},
    ))
    assert serializer.is_valid(), serializer.errors
    parameters = serializer.object
    parameter_values = {}

    with pytest.raises(ValidationError) as err:
        validate_parameters(parameter_values, parameters, inner=True)

    assert 'id' in err.value.messages[0]
    assert 'required' in err.value.messages[0]['id'][0]
    assert_error_message_equal(
        err.value.messages[0]['id'][0]['required'][0],
        MESSAGES['required']['required'],
    )


def test_parameters_allowed_missing_when_not_required():
    serializer = ParameterSerializer(many=True, data=(
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
    ))
    assert serializer.is_valid(), serializer.errors
    parameters = serializer.object
    parameter_values = {}

    validate_parameters(parameter_values, parameters, inner=True)

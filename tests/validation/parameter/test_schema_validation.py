import pytest

from flex.exceptions import ValidationError
from flex.serializers.core import ParameterSerializer
from flex.validation.parameter import (
    validate_parameters,
)
from flex.constants import (
    BODY,
    STRING,
    INTEGER,
    INT32,
)
from flex.error_messages import MESSAGES

from tests.utils import assert_error_message_equal


@pytest.mark.parametrize(
    'value,error_key,message_key',
    (
        ('not-a-uuid', 'format', 'invalid_uuid'), # not a valid uuid.
        (1234, 'type', 'invalid'), # not a string.
    ),
)
def test_parameter_schema_as_reference_validation_for_invalid_value(value, error_key, message_key):
    context = {
        'definitions': {'UUID': {'type': STRING, 'format': 'uuid'}},
    }
    serializer = ParameterSerializer(many=True, context=context, data=(
        {
            'name': 'id',
            'in': BODY,
            'description': 'id',
            'required': True,
            'schema': {'$ref': 'UUID'},
        },
    ))
    assert serializer.is_valid(), serializer.errors
    parameters = serializer.object
    parameter_values = {
        'id': value,
    }

    with pytest.raises(ValidationError) as err:
        validate_parameters(parameter_values, parameters, context=context, inner=True)

    assert 'id' in err.value.messages[0]
    assert error_key in err.value.messages[0]['id'][0]
    assert_error_message_equal(
        err.value.messages[0]['id'][0][error_key][0],
        MESSAGES[error_key][message_key],
    )


@pytest.mark.parametrize(
    'value,error_key,message_key',
    (
        ('not-a-uuid', 'format', 'invalid_uuid'), # not a valid uuid.
        (1234, 'type', 'invalid'), # not a string.
    ),
)
def test_parameter_schema_validation_for_invalid_value(value, error_key, message_key):
    serializer = ParameterSerializer(many=True, data=(
        {
            'name': 'id',
            'in': BODY,
            'description': 'id',
            'required': True,
            'schema': {'type': STRING, 'format': 'uuid'},
        },
    ))
    assert serializer.is_valid(), serializer.errors
    parameters = serializer.object
    parameter_values = {
        'id': value,
    }

    with pytest.raises(ValidationError) as err:
        validate_parameters(parameter_values, parameters, context={}, inner=True)

    assert 'id' in err.value.messages[0]
    assert error_key in err.value.messages[0]['id'][0]
    assert_error_message_equal(
        err.value.messages[0]['id'][0][error_key][0],
        MESSAGES[error_key][message_key],
    )


@pytest.mark.parametrize(
    'value',
    (
        1234,
        5678,
    ),
)
def test_local_parameter_values_override_schema(value):
    serializer = ParameterSerializer(many=True, data=(
        {
            'name': 'id',
            'in': BODY,
            'description': 'id',
            'required': True,
            'type': INTEGER,
            'format': INT32,
            'schema': {'type': STRING, 'format': 'uuid'},
        },
    ))
    assert serializer.is_valid(), serializer.errors
    parameters = serializer.object
    parameter_values = {
        'id': value,
    }

    validate_parameters(parameter_values, parameters, context={}, inner=True)


@pytest.mark.parametrize(
    'value',
    (
        'http://www.example.com',
        'http://google.com',
        'https://facebook.com',
    ),
)
def test_parameter_schema_validation_on_valid_values(value):
    serializer = ParameterSerializer(many=True, data=(
        {
            'name': 'id',
            'in': BODY,
            'description': 'id',
            'required': True,
            'schema': {
                'type': STRING,
                'format': 'uri',
            },
        },
    ))
    assert serializer.is_valid(), serializer.errors
    parameters = serializer.object
    parameter_values = {
        'id': value,
    }

    validate_parameters(parameter_values, parameters, context={}, inner=True)

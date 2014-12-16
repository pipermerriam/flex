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
)
from flex.error_messages import MESSAGES

from tests.utils import assert_error_message_equal


#
# minimum validation tests
#
@pytest.mark.parametrize(
    'min_items,value',
    (
        (1, []),
        (2, ['a']),
        (5, ['1', '2', '3', '4']),
    ),
)
def test_min_items_on_values_with_too_few_items(min_items, value):
    serializer = ParameterSerializer(many=True, data=[
        {
            'name': 'id',
            'in': PATH,
            'description':'id',
            'type': ARRAY,
            'required': True,
            'minItems': min_items,
            'items': {'type': STRING},
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
    assert 'minItems' in err.value.messages[0]['id'][0]
    assert_error_message_equal(
        err.value.messages[0]['id'][0]['minItems'][0],
        MESSAGES['min_items']['invalid'],
    )


@pytest.mark.parametrize(
    'min_items,value',
    (
        (1, ['a']),
        (1, ['a', 'b']),
        (3, ['1', '2', '3', '4']),
    ),
)
def test_min_items_on_values_with_valid_array_length(min_items, value):
    serializer = ParameterSerializer(many=True, data=[
        {
            'name': 'id',
            'in': PATH,
            'description':'id',
            'type': ARRAY,
            'required': True,
            'minItems': min_items,
            'items': {'type': STRING},
        },
    ])
    assert serializer.is_valid(), serializer.errors
    parameters = serializer.save()
    parameter_values = {
        'id': value,
    }

    validate_parameters(parameter_values, parameters, {}, inner=True)


#
# maximum validation tests
#
@pytest.mark.parametrize(
    'max_items,value',
    (
        (1, ['a', 'b']),
        (2, ['1', '2', '3']),
        (5, ['1', '2', '3', '4', '5', '6']),
    ),
)
def test_max_items_on_values_with_too_many_items(max_items, value):
    serializer = ParameterSerializer(many=True, data=[
        {
            'name': 'id',
            'in': PATH,
            'description':'id',
            'type': ARRAY,
            'required': True,
            'maxItems': max_items,
            'items': {'type': STRING},
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
    assert 'maxItems' in err.value.messages[0]['id'][0]
    assert_error_message_equal(
        err.value.messages[0]['id'][0]['maxItems'][0],
        MESSAGES['max_items']['invalid'],
    )


@pytest.mark.parametrize(
    'max_items,value',
    (
        (1, []),
        (1, ['a']),
        (2, ['a', 'b']),
        (5, ['1', '2', '3', '4']),
    ),
)
def test_max_items_on_values_with_valid_array_length(max_items, value):
    serializer = ParameterSerializer(many=True, data=[
        {
            'name': 'id',
            'in': PATH,
            'description':'id',
            'type': ARRAY,
            'required': True,
            'maxItems': max_items,
            'items': {'type': STRING},
        },
    ])
    assert serializer.is_valid(), serializer.errors
    parameters = serializer.save()
    parameter_values = {
        'id': value,
    }

    validate_parameters(parameter_values, parameters, {}, inner=True)

import pytest

from flex.serializers.core import ParameterSerializer
from flex.constants import (
    INTEGER,
    NUMBER,
    BOOLEAN,
    ARRAY,
    QUERY,
    CSV,
    SSV,
    TSV,
    PIPES,
)
from flex.validation.parameter import (
    type_cast_parameters,
)


#
# type_cast_parameters tests
#
def test_integer_type_casting():
    serializer = ParameterSerializer(data=[{
        'type': INTEGER,
        'in': QUERY,
        'description': 'id',
        'name': 'id',
    }])
    assert serializer.is_valid(), serializer.errors
    parameters = {'id': '123'}
    actual = type_cast_parameters(parameters, serializer.object, {})
    assert actual['id'] == 123


def test_number_type_casting():
    serializer = ParameterSerializer(data=[{
        'type': NUMBER,
        'in': QUERY,
        'description': 'id',
        'name': 'id',
    }])
    assert serializer.is_valid(), serializer.errors
    parameters = {'id': '12.5'}
    actual = type_cast_parameters(parameters, serializer.object, {})
    assert actual['id'] == 12.5


@pytest.mark.parametrize(
    'input_,expected',
    (
        ('true', True),
        ('True', True),
        ('1', True),
        ('false', False),
        ('False', False),
        ('0', False),
        ('', False),
    )
)
def test_boolean_type_casting(input_, expected):
    serializer = ParameterSerializer(data=[{
        'type': BOOLEAN,
        'in': QUERY,
        'description': 'id',
        'name': 'id',
    }])
    assert serializer.is_valid(), serializer.errors
    parameters = {'id': input_}
    actual = type_cast_parameters(parameters, serializer.object, {})
    assert actual['id'] == expected


@pytest.mark.parametrize(
    'format_,value',
    (
        (CSV, '1,2,3'),
        (CSV, '1, 2, 3'),
        (SSV, '1 2 3'),
        (SSV, '1 2  3'),
        (TSV, '1\t2\t3'),
        (TSV, '1\t 2\t 3'),
        (PIPES, '1|2|3'),
        (PIPES, '1| 2| 3'),
    )
)
def test_array_type_casting(format_, value):
    serializer = ParameterSerializer(data=[{
        'type': ARRAY,
        'collectionFormat': format_,
        'in': QUERY,
        'description': 'id',
        'name': 'id',
        'items': {'type': INTEGER},
    }])
    assert serializer.is_valid(), serializer.errors
    parameters = {'id': value}
    actual = type_cast_parameters(parameters, serializer.object, {})
    assert actual['id'] == [1, 2, 3]

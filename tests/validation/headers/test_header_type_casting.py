import pytest

from flex.serializers.core import HeaderSerializer
from flex.validation.common import generate_value_processor
from flex.constants import (
    INTEGER,
    NUMBER,
    BOOLEAN,
    ARRAY,
    STRING,
    CSV,
    SSV,
    TSV,
    PIPES,
)


def test_integer_header_type():
    serializer = HeaderSerializer(
        data={
            'type': INTEGER,
        }
    )
    assert serializer.is_valid(), serializer.errors
    value_processor = generate_value_processor(context={}, **serializer.save())

    actual = value_processor('123')
    expected = 123
    assert actual == expected


@pytest.mark.parametrize(
    'value',
    (
        '1.2', # Non integer
        'abc', # Non number
    )
)
def test_integer_header_type_with_invalid_values(value):
    serializer = HeaderSerializer(
        data={
            'type': INTEGER,
        }
    )
    assert serializer.is_valid(), serializer.errors
    value_processor = generate_value_processor(context={}, **serializer.save())

    actual = value_processor(value)
    assert actual == value


def test_number_header_type():
    serializer = HeaderSerializer(
        data={
            'type': NUMBER,
        }
    )
    assert serializer.is_valid(), serializer.errors
    value_processor = generate_value_processor(context={}, **serializer.save())

    actual = value_processor('10.5')
    expected = 10.5
    assert actual == expected


def test_number_header_type_with_invalid_value():
    serializer = HeaderSerializer(
        data={
            'type': NUMBER,
        }
    )
    assert serializer.is_valid(), serializer.errors
    value_processor = generate_value_processor(context={}, **serializer.save())

    actual = value_processor('abc')
    assert actual == 'abc'


@pytest.mark.parametrize(
    'input_,expected',
    (
        ('true', True),
        ('True', True),
        ('false', False),
        ('False', False),
        ('1', True),
        ('0', False),
        ('', False),
    )
)
def test_boolean_header_type(input_, expected):
    serializer = HeaderSerializer(
        data={
            'type': BOOLEAN,
        }
    )
    assert serializer.is_valid(), serializer.errors
    value_processor = generate_value_processor(context={}, **serializer.save())

    actual = value_processor(input_)
    assert actual == expected


def test_boolean_header_type_for_invalid_value():
    serializer = HeaderSerializer(
        data={
            'type': BOOLEAN,
        }
    )
    assert serializer.is_valid(), serializer.errors
    value_processor = generate_value_processor(context={}, **serializer.save())

    actual = value_processor('not-a-known-boolean')
    assert actual == 'not-a-known-boolean'


@pytest.mark.parametrize(
    'format_,input_',
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
def test_array_header_type_casting_with_single_tems(format_, input_):
    serializer = HeaderSerializer(
        data={
            'type': ARRAY,
            'collectionFormat': format_,
            'items': {'type': INTEGER}
        }
    )
    assert serializer.is_valid(), serializer.errors
    value_processor = generate_value_processor(context={}, **serializer.save())

    actual = value_processor(input_)
    expected = [1, 2, 3]
    assert actual == expected


def test_array_header_type_casting_with_multiple_items():
    serializer = HeaderSerializer(
        data={
            'type': ARRAY,
            'collectionFormat': CSV,
            'items': [
                {'type': INTEGER},
                {'type': STRING},
                {'type': BOOLEAN},
            ]
        }
    )
    assert serializer.is_valid(), serializer.errors
    value_processor = generate_value_processor(context={}, **serializer.save())

    actual = value_processor('1,a,true,2')
    expected = [1, 'a', True, '2']
    assert actual == expected

import pytest

from flex.serializers.definitions import SchemaSerializer
from flex.constants import (
    NULL,
    BOOLEAN,
    INTEGER,
    NUMBER,
    STRING,
    ARRAY,
    OBJECT,
)

from tests.utils import assert_error_message_equal


def test_empty_schema_is_valid():
    schema = {}

    serializer = SchemaSerializer(data=schema)

    assert serializer.is_valid()


def test_schema_reference_is_placed_in_deferred_refrences():
    context = {'deferred_references': set()}
    serializer = SchemaSerializer(
        data={'$ref': 'SomeReference'},
        context=context,
    )
    assert serializer.is_valid()
    assert 'SomeReference' in serializer.context['deferred_references']


def test_schema_item_references_are_deferred():
    context = {'deferred_references': set()}
    serializer = SchemaSerializer(
        data={'items': ['SomeReference']},
        context=context,
    )
    assert serializer.is_valid()
    assert 'SomeReference' in serializer.context['deferred_references']


#
# minimum validation tests
#
@pytest.mark.parametrize(
    'type_',
    (NULL, BOOLEAN, STRING, ARRAY, OBJECT),
)
def test_minimum_is_invalid_for_non_numeric_types(type_):
    serializer = SchemaSerializer(
        data={
            'type': type_,
            'minimum': 0,
        },
    )
    assert not serializer.is_valid()
    assert 'minimum' in serializer.errors
    assert_error_message_equal(
        serializer.errors['minimum'][0],
        serializer.error_messages['invalid_type_for_minimum'],
    )


@pytest.mark.parametrize(
    'type_',
    (INTEGER, NUMBER),
)
def test_minimum_is_valid_with_numeric_types(type_):
    serializer = SchemaSerializer(
        data={
            'type': type_,
            'minimum': 0,
        },
    )
    assert 'minimum' not in serializer.errors


#
# maximum validation tests
#
@pytest.mark.parametrize(
    'type_',
    (NULL, BOOLEAN, STRING, ARRAY, OBJECT),
)
def test_maximum_is_invalid_for_non_numeric_types(type_):
    serializer = SchemaSerializer(
        data={
            'type': type_,
            'maximum': 0,
        },
    )
    assert not serializer.is_valid()
    assert 'maximum' in serializer.errors
    assert_error_message_equal(
        serializer.errors['maximum'][0],
        serializer.error_messages['invalid_type_for_maximum'],
    )


@pytest.mark.parametrize(
    'type_',
    (INTEGER, NUMBER),
)
def test_maximum_is_valid_with_numeric_types(type_):
    serializer = SchemaSerializer(
        data={
            'type': type_,
            'maximum': 0,
        },
    )
    assert 'maximum' not in serializer.errors

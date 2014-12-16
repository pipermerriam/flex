import pytest

from flex.error_messages import MESSAGES
from flex.serializers.definitions import (
    SchemaSerializer,
    ItemsSerializer,
)

from flex.constants import (
    ARRAY,
    INTEGER,
    STRING,
)

from tests.utils import (
    assert_error_message_equal,
    assert_message_in_errors,
)


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
# items validation
#
@pytest.mark.parametrize(
    'items',
    (
        1234,  # integer
        1.234,  # number
        True,  # boolean
        None,  # null
    ),
)
def test_items_invalid_when_not_array_or_object_or_reference(items):
    schema = {
        'type': ARRAY,
        'items': [items],
    }

    serializer = SchemaSerializer(
        data=schema,
    )

    assert not serializer.is_valid()
    assert_message_in_errors(
        MESSAGES['items']['invalid_type'],
        serializer.errors,
    )


def test_items_detects_invalid_single_schema():
    schema = {
        'type': ARRAY,
        'items': {
            'type': INTEGER,
            'minLength': 4,  # invalid with type 'integer'
        },
    }

    serializer = SchemaSerializer(
        data=schema,
    )

    assert not serializer.is_valid()
    assert_message_in_errors(
        serializer.error_messages['invalid_type_for_min_length'],
        serializer.errors,
        'items.minLength',
    )


def test_items_with_valid_singular_schema():
    schema = {
        'type': ARRAY,
        'items': {
            'type': INTEGER,
            'minimum': 4,
        },
    }

    serializer = SchemaSerializer(
        data=schema,
    )

    serializer.is_valid()
    assert 'items' not in serializer.errors


def test_items_detects_invalid_schema_in_array():
    schema = {
        'type': ARRAY,
        'items': [
            {
                'type': INTEGER,
                'minLength': 4,  # invalid with type 'integer'
            },
            {
                'type': STRING,
                'minimum': 4,  # invalid with type 'string'
            },
        ]
    }

    serializer = SchemaSerializer(
        data=schema,
    )

    assert not serializer.is_valid()
    assert 'items' in serializer.errors
    assert 'minLength' in serializer.errors['items'][0]
    assert_error_message_equal(
        serializer.errors['items'][0]['minLength'][0],
        serializer.error_messages['invalid_type_for_min_length'],
    )
    assert 'minimum' in serializer.errors['items'][1]
    assert_error_message_equal(
        serializer.errors['items'][1]['minimum'][0],
        serializer.error_messages['invalid_type_for_minimum'],
    )


def test_items_with_array_of_valid_schemas():
    schema = {
        'type': ARRAY,
        'items': [
            {
                'type': INTEGER,
                'minimum': 4,
            },
            {
                'type': STRING,
                'minLength': 4,
            },
        ]
    }

    serializer = SchemaSerializer(
        data=schema,
    )

    serializer.is_valid()
    assert 'items' not in serializer.errors


def test_items_with_mixed_array_of_references_and_schemas():
    schema = {
        'type': ARRAY,
        'items': [
            {
                'type': INTEGER,
                'minimum': 4,
            },
            'SomeReference',
            {
                'type': STRING,
                'minLength': 4,
            },
        ]
    }

    serializer = SchemaSerializer(
        data=schema,
        context={'deferred_references': set()}
    )

    serializer.is_valid()
    assert 'items' not in serializer.errors

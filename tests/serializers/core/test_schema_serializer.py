import pytest

from flex.error_messages import MESSAGES
from flex.serializers.core import (
    SchemaSerializer,
)
from flex.constants import (
    INTEGER,
    ARRAY,
    STRING,
)

from tests.utils import (
    assert_error_message_equal,
    assert_message_in_errors,
)


#
# $ref validation tests
#
def test_unknown_schema_reference():
    schema = {
        '$ref': 'SomeReference',
    }
    serializer = SchemaSerializer(
        data=schema,
        context={},
    )

    assert not serializer.is_valid()
    assert '$ref' in serializer.errors
    assert_error_message_equal(
        serializer.errors['$ref'][0],
        serializer.error_messages['unknown_reference']
    )


def test_valid_reference():
    schema = {
        '$ref': 'SomeReference',
    }
    serializer = SchemaSerializer(
        data=schema,
        context={
            'definitions': {'SomeReference': {}},
        },
    )

    assert serializer.is_valid()


#
# items validation tests
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
    assert 'items' in serializer.errors
    assert 'non_field_errors' in serializer.errors['items'][0][0]
    assert_error_message_equal(
        serializer.errors['items'][0][0]['non_field_errors'],
        MESSAGES['items']['invalid_type'],
    )


def test_items_as_missing_reference():
    schema = {
        'type': ARRAY,
        'items': 'SomeReference',
    }
    serializer = SchemaSerializer(
        data=schema,
    )
    assert not serializer.is_valid()
    assert 'items' in serializer.errors
    assert_error_message_equal(
        serializer.errors['items'][0],
        serializer.error_messages['unknown_reference'],
    )


def test_items_as_existing_reference():
    schema = {
        'type': ARRAY,
        'items': 'SomeReference',
    }
    serializer = SchemaSerializer(
        data=schema,
        context={
            'definitions': {'SomeReference': {}},
        },
    )
    serializer.is_valid()
    assert 'items' not in serializer.errors


def test_items_validated_as_valid_schema_object():
    schema = {
        'type': ARRAY,
        'items': {
            'type': 'unknown-type',
        }
    }
    serializer = SchemaSerializer(
        data=schema,
    )
    assert not serializer.is_valid()
    assert_message_in_errors(
        MESSAGES['type']['unknown'],
        serializer.errors,
    )


def test_items_as_array_of_invalid_schemas():
    schema = {
        'items': [
            {'type': 'unknown-type'},
            {'minLength': -1},
        ],
    }
    serializer = SchemaSerializer(
        data=schema,
    )
    assert not serializer.is_valid()
    assert 'items' in serializer.errors
    assert 'type' in serializer.errors['items'][0]
    assert 'minLength' in serializer.errors['items'][1]


def test_items_as_array_of_valid_schemas():
    schema = {
        'type': ARRAY,
        'items': [
            {'type': INTEGER},
            {'minLength': 3},
        ],
    }
    serializer = SchemaSerializer(
        data=schema,
    )
    serializer.is_valid()
    assert 'items' not in serializer.errors


def test_items_as_array_of_references_with_missing_reference():
    schema = {
        'type': ARRAY,
        'items': ['SomeReference', 'SomeOtherReference']
    }
    serializer = SchemaSerializer(
        data=schema,
        context={
            'definitions': {'SomeReference': {}},
        },
    )
    assert not serializer.is_valid()
    assert_message_in_errors(
        MESSAGES['unknown_reference']['definition'],
        serializer.errors,
    )


def test_items_as_array_of_valid_references():
    schema = {
        'type': ARRAY,
        'items': ['SomeReference', 'SomeOtherReference']
    }
    serializer = SchemaSerializer(
        data=schema,
        context={
            'definitions': {
                'SomeReference': {},
                'SomeOtherReference': {},
            },
        },
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
        context={'definitions': {'SomeReference': {}}}
    )

    serializer.is_valid()
    assert 'items' not in serializer.errors

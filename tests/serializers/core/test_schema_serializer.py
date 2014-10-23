from flex.serializers.core import SchemaSerializer
from flex.constants import INTEGER

from tests.utils import assert_error_message_equal

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
def test_items_as_missing_reference():
    schema = {
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
        'items': 'SomeReference',
    }
    serializer = SchemaSerializer(
        data=schema,
        context={
            'definitions': {'SomeReference': {}},
        },
    )
    assert 'items' not in serializer.errors


def test_items_validated_as_valid_schema_object():
    schema = {
        'items': {
            'type': 'unknown-type',
        }
    }
    serializer = SchemaSerializer(
        data=schema,
    )
    assert not serializer.is_valid()
    assert 'items' in serializer.errors
    assert 'type' in serializer.errors['items'][0]


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
        'items': [
            {'type': INTEGER},
            {'minLength': 3},
        ],
    }
    serializer = SchemaSerializer(
        data=schema,
    )
    assert 'items' not in serializer.errors


def test_items_as_array_of_references_with_missing_reference():
    schema = {
        'items': ['SomeReference', 'SomeOtherReference']
    }
    serializer = SchemaSerializer(
        data=schema,
        context={
            'definitions': {'SomeReference': {}},
        },
    )
    assert not serializer.is_valid()
    assert 'items' in serializer.errors
    assert 'SomeOtherReference' in serializer.errors['items'][0]
    assert_error_message_equal(
        serializer.errors['items'][0],
        serializer.error_messages['unknown_reference'],
    )


def test_items_as_array_of_valid_references():
    schema = {
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
    assert 'items' not in serializer.errors

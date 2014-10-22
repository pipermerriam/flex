from flex.serializers.core import SchemaSerializer

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

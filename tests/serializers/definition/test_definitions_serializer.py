from flex.serializers.definitions import (
    DefinitionsSerializer,
)

from tests.utils import assert_error_message_equal


def test_reference_within_reference():
    serializer = DefinitionsSerializer(
        data={
            'Node': {
                'properties': {
                    'parent': {'$ref': 'Unknown'},
                },
            },
        },
        context={'deferred_references': set()},
    )
    assert not serializer.is_valid()
    assert 'non_field_errors' in serializer.errors
    assert_error_message_equal(
        serializer.errors['non_field_errors'][0],
        serializer.error_messages['unknown_references'],
    )

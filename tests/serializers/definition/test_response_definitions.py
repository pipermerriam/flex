from flex.serializers.definitions import (
    HeaderSerializer,
)

from flex.constants import (
    ARRAY,
    INTEGER,
)


def test_schema_reference_is_placed_in_deferred_refrences():
    context = {'deferred_references': set()}
    serializer = HeaderSerializer(
        data={'type': INTEGER, 'schema': 'SomeReference'},
        context=context,
    )
    assert serializer.is_valid(), serializer.errors
    assert 'SomeReference' in serializer.context['deferred_references']


def test_schema_item_references_are_deferred():
    context = {'deferred_references': set()}
    serializer = HeaderSerializer(
        data={'type': ARRAY, 'items': ['SomeReference']},
        context=context,
    )
    assert serializer.is_valid(), serializer.errors
    assert 'SomeReference' in serializer.context['deferred_references']

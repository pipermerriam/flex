from flex.serializers.definitions import (
    SchemaSerializer,
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

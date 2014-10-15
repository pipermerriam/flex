from flex.serializers.definitions import (
    SwaggerDefinitionsSerializer,
)


def test_no_definitions():
    serializer = SwaggerDefinitionsSerializer(data={})

    assert serializer.is_valid()

from flex.serializers.definitions import (
    ParameterDefinitionsSerializer,
)
from flex.constants import (
    PATH,
    INTEGER,
)


def test_invalid_list_of_references():
    data = {
        'Id': [{'name': 'id', 'in': PATH, 'description': 'id', 'type': INTEGER, 'required': True}],
    }
    serializer = ParameterDefinitionsSerializer(
        data=data,
    )
    assert not serializer.is_valid(), serializer.object

from flex.serializers.common import (
    HomogenousDictSerializer,
)

from rest_framework import serializers


class RoleSerializer(serializers.Serializer):
    """
    Test serializer to serve as the fields for the RolesSerializer
    """
    name = serializers.CharField()
    age = serializers.IntegerField()


class RolesSerializer(HomogenousDictSerializer):
    """
    Test serializer to test the functionality of the HomogenousDictSerializer
    """
    value_serializer_class = RoleSerializer


def test_autopopulates_fields_based_on_data():
    data = {
        'field_a': {'name': 'Field A', 'age': 10},
        'field_b': {'name': 'Field b', 'age': 20},
    }
    serializer = RolesSerializer(data=data)
    assert serializer.is_valid(), serializer.errors

    assert 'field_a' in serializer.fields
    assert 'field_b' in serializer.fields


class ParentSerializer(serializers.Serializer):
    roles = RolesSerializer()


def test_autopopulates_when_used_as_a_field():
    data = {
        'roles': {
            'field_a': {'name': 'Field A', 'age': 10},
            'field_b': {'name': 'Field b', 'age': 20},
        },
    }
    serializer = ParentSerializer(data=data)
    assert serializer.is_valid(), serializer.errors

    field = serializer.fields['roles']
    assert 'field_a' in field.fields
    assert 'field_b' in field.fields

    assert serializer.is_valid(), serializer.errors
    try:
        ret = serializer.validated_data
    except AttributeError:
        ret = serializer.object

    roles = ret.get('roles', {})
    assert 'field_a' in roles
    assert 'field_b' in roles

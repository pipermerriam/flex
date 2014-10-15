import pytest

from rest_framework import serializers

from flex.utils import is_non_string_iterable
from flex.serializers.fields import (
    MaybeListCharField,
    SecurityRequirementReferenceField,
)

from tests.utils import assert_error_message_equal


#
# MaybeListCharField tests
#
def test_maybe_list_char_field_accepts_strings():
    field = MaybeListCharField()
    data = {'foo': 'a-string'}
    into = {}
    field.field_from_native(data, {}, 'foo', into)
    assert data['foo'] == into.get('foo')


def test_maybe_list_char_field_accepts_lists():
    field = MaybeListCharField()
    data = {'foo': ['a-string', 'another-string']}
    into = {}
    field.field_from_native(data, {}, 'foo', into)
    assert data['foo'] == into.get('foo')


def test_maybe_list_char_field_runs_validators_on_singular_strings():
    def validator(value):
        if is_non_string_iterable(value):
            if not all([v.startswith('bar') for v in value]):
                raise serializers.ValidationError('error')
        else:
            if not value.startswith('bar'):
                raise serializers.ValidationError('error')

    field = MaybeListCharField(validators=[validator])
    data = {'foo': 'not-bar'}
    into = {}
    with pytest.raises(serializers.ValidationError):
        field.field_from_native(data, {}, 'foo', into)


def test_maybe_list_char_field_runs_validators_on_lists():
    def validator(value):
        if is_non_string_iterable(value):
            if not all([v.startswith('bar') for v in value]):
                raise serializers.ValidationError('error')
        else:
            if not value.startswith('bar'):
                raise serializers.ValidationError('error')

    field = MaybeListCharField(validators=[validator])
    data = {'foo': ['a-string', 'another-string']}
    into = {}
    with pytest.raises(serializers.ValidationError):
        field.field_from_native(data, {}, 'foo', into)


#
# SecurityRequirementReferenceField tests
#
def test_invalid_with_unknown_reference():
    class TestSerializer(serializers.Serializer):
        foo = SecurityRequirementReferenceField()

    serializer = TestSerializer(
        data={'foo': 'SomeReference'},
        context={
            'securityDefinitions': {},
        },
    )

    assert not serializer.is_valid()
    assert 'foo' in serializer.errors
    assert_error_message_equal(
        serializer.errors['foo'][0],
        SecurityRequirementReferenceField.default_error_messages['unknown_reference'],
    )


def test_valid_with_known_reference():
    class TestSerializer(serializers.Serializer):
        foo = SecurityRequirementReferenceField()

    serializer = TestSerializer(
        data={'foo': 'SomeReference'},
        context={
            'securityDefinitions': {'SomeReference': {}},
        },
    )

    assert serializer.is_valid()

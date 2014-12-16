import pytest

from flex.error_messages import MESSAGES
from flex.utils import is_non_string_iterable
from flex.serializers.fields import (
    MaybeListCharField,
    SecurityRequirementReferenceField,
)
from flex.exceptions import ValidationError

from rest_framework import serializers

from tests.utils import assert_error_message_equal


class TestSerializer(serializers.Serializer):
    test_field = MaybeListCharField()

def get_validated_data(serializer):
    assert serializer.is_valid(), serializer.errors

    try:
        return serializer.validated_data
    except AttributeError:
        return serializer.object


#
# MaybeListCharField tests
#
def test_maybe_list_char_field_accepts_strings():
    data = {'test_field': 'a-string'}
    serializer = TestSerializer(data=data)
    actual = get_validated_data(serializer)
    assert actual['test_field'] == 'a-string'


def test_maybe_list_char_field_accepts_lists():
    data = {'test_field': ['a-string', 'another-string']}
    serializer = TestSerializer(data=data)
    actual = get_validated_data(serializer)
    assert actual['test_field'] == ['a-string', 'another-string']


def test_maybe_list_char_field_runs_validators_on_singular_strings():
    def validator(value):
        if is_non_string_iterable(value):
            if not all([v.startswith('bar') for v in value]):
                raise ValidationError('error')
        else:
            if not value.startswith('bar'):
                raise ValidationError('error')

    class WithValidatorSerializer(serializers.Serializer):
        test_field = MaybeListCharField(validators=[validator])

    data = {'test_field': 'not-bar'}
    serializer = WithValidatorSerializer(data=data)
    with pytest.raises(AssertionError):
        get_validated_data(serializer)


def test_maybe_list_char_field_runs_validators_on_lists():
    def validator(value):
        if is_non_string_iterable(value):
            if not all([v.startswith('bar') for v in value]):
                raise ValidationError('error')
        else:
            if not value.startswith('bar'):
                raise ValidationError('error')

    class WithValidatorSerializer(serializers.Serializer):
        test_field = MaybeListCharField(validators=[validator])

    data = {'test_field': ['a-string', 'another-string']}
    serializer = WithValidatorSerializer(data=data)
    with pytest.raises(AssertionError):
        get_validated_data(serializer)


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
        MESSAGES['unknown_reference']['security'],
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

    assert serializer.is_valid(), serializer.errors

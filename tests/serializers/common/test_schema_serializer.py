import pytest

from flex.serializers.definitions import BaseSchemaSerializer
from flex.constants import (
    NULL,
    BOOLEAN,
    INTEGER,
    NUMBER,
    STRING,
    ARRAY,
    OBJECT,
)

from tests.utils import assert_error_message_equal


#
# minimum validation tests
#
@pytest.mark.parametrize(
    'type_',
    (NULL, BOOLEAN, STRING, ARRAY, OBJECT),
)
def test_minimum_is_invalid_for_non_numeric_types(type_):
    serializer = BaseSchemaSerializer(
        data={
            'type': type_,
            'minimum': 0,
        },
    )
    assert not serializer.is_valid()
    assert 'minimum' in serializer.errors
    assert_error_message_equal(
        serializer.errors['minimum'][0],
        serializer.error_messages['invalid_type_for_minimum'],
    )


@pytest.mark.parametrize(
    'type_',
    (INTEGER, NUMBER),
)
def test_minimum_is_valid_with_numeric_types(type_):
    serializer = BaseSchemaSerializer(
        data={
            'type': type_,
            'minimum': 0,
        },
    )
    assert 'minimum' not in serializer.errors


#
# maximum validation tests
#
@pytest.mark.parametrize(
    'type_',
    (NULL, BOOLEAN, STRING, ARRAY, OBJECT),
)
def test_maximum_is_invalid_for_non_numeric_types(type_):
    serializer = BaseSchemaSerializer(
        data={
            'type': type_,
            'maximum': 0,
        },
    )
    assert not serializer.is_valid()
    assert 'maximum' in serializer.errors
    assert_error_message_equal(
        serializer.errors['maximum'][0],
        serializer.error_messages['invalid_type_for_maximum'],
    )


@pytest.mark.parametrize(
    'type_',
    (INTEGER, NUMBER),
)
def test_maximum_is_valid_with_numeric_types(type_):
    serializer = BaseSchemaSerializer(
        data={
            'type': type_,
            'maximum': 0,
        },
    )
    assert 'maximum' not in serializer.errors


#
# exclusiveMinimum tests
#
def test_exclusive_minimum_requires_minimum():
    serializer = BaseSchemaSerializer(
        data={
            #'maximum': 0,  # Intentionally commented out to show it's missing from data.
            'exclusiveMinimum': True
        },
    )
    assert not serializer.is_valid()
    assert 'exclusiveMinimum' in serializer.errors
    assert_error_message_equal(
        serializer.errors['exclusiveMinimum'][0],
        serializer.error_messages['exclusive_minimum_requires_minimum'],
    )


def test_exclusive_minimum_with_minimum_is_valid():
    serializer = BaseSchemaSerializer(
        data={
            'minimum': 0,
            'exclusiveMinimum': True
        },
    )
    assert 'exclusiveMinimum' not in serializer.errors


#
# exclusiveMaximum tests
#
def test_exclusive_maximum_requires_maximum():
    serializer = BaseSchemaSerializer(
        data={
            #'maximum': 0,  # Intentionally commented out to show it's missing from data.
            'exclusiveMaximum': True
        },
    )
    assert not serializer.is_valid()
    assert 'exclusiveMaximum' in serializer.errors
    assert_error_message_equal(
        serializer.errors['exclusiveMaximum'][0],
        serializer.error_messages['exclusive_maximum_requires_maximum'],
    )


def test_exclusive_maximum_with_maximum_is_valid():
    serializer = BaseSchemaSerializer(
        data={
            'maximum': 0,
            'exclusiveMaximum': True
        },
    )
    assert 'exclusiveMaximum' not in serializer.errors


#
# multipleOf validation tests
#
@pytest.mark.parametrize(
    'type_',
    (
        NULL,
        BOOLEAN,
        STRING,
        ARRAY,
        OBJECT,
    ),
)
def test_multiple_of_invalid_with_non_number_types(type_):
    serializer = BaseSchemaSerializer(
        data={
            'type': type_,
            'multipleOf': 10,
        },
    )
    assert not serializer.is_valid()
    assert 'multipleOf' in serializer.errors
    assert_error_message_equal(
        serializer.errors['multipleOf'][0],
        serializer.error_messages['invalid_type_for_multiple_of'],
    )


@pytest.mark.parametrize(
    'type_',
    (INTEGER, NUMBER),
)
def test_multiple_of_valid_for_json_number_types(type_):
    serializer = BaseSchemaSerializer(
        data={
            'type': type_,
            'multipleOf': 10,
        },
    )
    assert 'multipleOf' not in serializer.errors


#
# minLength validation tests
#
@pytest.mark.parametrize(
    'type_',
    (
        NULL,
        BOOLEAN,
        INTEGER,
        NUMBER,
        ARRAY,
        OBJECT,
    ),
)
def test_min_length_invalid_with_non_string_types(type_):
    serializer = BaseSchemaSerializer(
        data={
            'type': type_,
            'minLength': 10,
        },
    )
    assert not serializer.is_valid()
    assert 'minLength' in serializer.errors
    assert_error_message_equal(
        serializer.errors['minLength'][0],
        serializer.error_messages['invalid_type_for_min_length'],
    )


def test_min_length_valid_with_string_type():
    serializer = BaseSchemaSerializer(
        data={
            'type': STRING,
            'minLength': 10,
        },
    )
    assert 'minLength' not in serializer.errors


#
# maxLength validation tests
#
@pytest.mark.parametrize(
    'type_',
    (
        NULL,
        BOOLEAN,
        INTEGER,
        NUMBER,
        ARRAY,
        OBJECT,
    ),
)
def test_max_length_invalid_with_non_string_types(type_):
    serializer = BaseSchemaSerializer(
        data={
            'type': type_,
            'maxLength': 10,
        },
    )
    assert not serializer.is_valid()
    assert 'maxLength' in serializer.errors
    assert_error_message_equal(
        serializer.errors['maxLength'][0],
        serializer.error_messages['invalid_type_for_max_length'],
    )


def test_max_length_valid_with_string_type():
    serializer = BaseSchemaSerializer(
        data={
            'type': STRING,
            'maxLength': 10,
        },
    )
    assert 'maxLength' not in serializer.errors

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


#
# maxItems tests
@pytest.mark.parametrize(
    'type_',
    (
        NULL,
        BOOLEAN,
        INTEGER,
        NUMBER,
        STRING,
        OBJECT,
    ),
)
def test_max_items_invalid_with_non_array_type(type_):
    serializer = BaseSchemaSerializer(
        data={
            'type': type_,
            'maxItems': 5,
        },
    )
    assert not serializer.is_valid()
    assert 'maxItems' in serializer.errors
    assert_error_message_equal(
        serializer.errors['maxItems'][0],
        serializer.error_messages['invalid_type_for_max_items'],
    )


def test_max_items_valid_with_array_type():
    serializer = BaseSchemaSerializer(
        data={
            'type': ARRAY,
            'maxItems': 5,
        },
    )
    assert 'maxItems' not in serializer.errors


#
# minItems tests
#
@pytest.mark.parametrize(
    'type_',
    (
        NULL,
        BOOLEAN,
        INTEGER,
        NUMBER,
        STRING,
        OBJECT,
    ),
)
def test_min_items_invalid_with_non_arraw_type(type_):
    serializer = BaseSchemaSerializer(
        data={
            'type': type_,
            'minItems': 5,
        },
    )
    assert not serializer.is_valid()
    assert 'minItems' in serializer.errors
    assert_error_message_equal(
        serializer.errors['minItems'][0],
        serializer.error_messages['invalid_type_for_min_items'],
    )


def test_min_items_valid_with_array_type():
    serializer = BaseSchemaSerializer(
        data={
            'type': ARRAY,
            'minItems': 5,
        },
    )
    assert 'minItems' not in serializer.errors


#
# uniqueItems tests
#
@pytest.mark.parametrize(
    'type_',
    (
        NULL,
        BOOLEAN,
        INTEGER,
        NUMBER,
        STRING,
        OBJECT,
    ),
)
def test_unique_items_invalid_with_non_arraw_type(type_):
    serializer = BaseSchemaSerializer(
        data={
            'type': type_,
            'uniqueItems': True,
        },
    )
    assert not serializer.is_valid()
    assert 'uniqueItems' in serializer.errors
    assert_error_message_equal(
        serializer.errors['uniqueItems'][0],
        serializer.error_messages['invalid_type_for_unique_items'],
    )


def test_unique_items_valid_with_array_type():
    serializer = BaseSchemaSerializer(
        data={
            'type': ARRAY,
            'uniqueItems': True,
        },
    )
    assert 'uniqueItems' not in serializer.errors


#
# enum tests
#
@pytest.mark.parametrize(
    'enum',
    (
        'abcd',
        {'a': 'foo', 'b': 'bar'},
        123,
        None,
    ),
)
def test_non_array_for_enum_is_invalid(enum):

    serializer = BaseSchemaSerializer(
        data={
            'enum': enum,
        },
    )
    assert not serializer.is_valid()
    assert 'enum' in serializer.errors


def test_valid_enum_iterable():

    serializer = BaseSchemaSerializer(
        data={
            'enum': ['a', 1, True, ['inner', 'array'], {'a': 'b', 'c': 'd'}, 2.0, None],
        },
    )
    assert 'enum' not in serializer.errors


#
# minProperties tests
#
@pytest.mark.parametrize(
    'type_',
    (
        NULL,
        BOOLEAN,
        INTEGER,
        NUMBER,
        STRING,
        ARRAY,
    ),
)
def test_min_properties_invalid_for_non_object_types(type_):
    serializer = BaseSchemaSerializer(
        data={
            'type': type_,
            'minProperties': 3,
        },
    )
    assert not serializer.is_valid()
    assert 'minProperties' in serializer.errors
    assert_error_message_equal(
        serializer.errors['minProperties'][0],
        serializer.error_messages['invalid_type_for_min_properties']
    )


def test_min_properties_valid_for_object_type():
    serializer = BaseSchemaSerializer(
        data={
            'type': OBJECT,
            'minProperties': 3,
        },
    )
    assert 'minProperties' not in serializer.errors


def test_min_properties_must_be_strictly_positive():
    serializer = BaseSchemaSerializer(
        data={
            'type': OBJECT,
            'minProperties': -1,
        },
    )
    assert not serializer.is_valid()
    assert 'minProperties' in serializer.errors
    assert serializer.errors['minProperties'][0].startswith(
        "Ensure this value is greater than or equal to",
    )


#
# maxProperties tests
#
@pytest.mark.parametrize(
    'type_',
    (
        NULL,
        BOOLEAN,
        INTEGER,
        NUMBER,
        STRING,
        ARRAY,
    ),
)
def test_max_properties_invalid_for_non_object_types(type_):
    serializer = BaseSchemaSerializer(
        data={
            'type': type_,
            'maxProperties': 3,
        },
    )
    assert not serializer.is_valid()
    assert 'maxProperties' in serializer.errors
    assert_error_message_equal(
        serializer.errors['maxProperties'][0],
        serializer.error_messages['invalid_type_for_max_properties']
    )


def test_max_properties_valid_for_object_type():
    serializer = BaseSchemaSerializer(
        data={
            'type': OBJECT,
            'maxProperties': 3,
        },
    )
    assert 'maxProperties' not in serializer.errors


def test_max_properties_must_be_strictly_positive():
    serializer = BaseSchemaSerializer(
        data={
            'type': OBJECT,
            'maxProperties': -1,
        },
    )
    assert not serializer.is_valid()
    assert 'maxProperties' in serializer.errors
    assert serializer.errors['maxProperties'][0].startswith(
        "Ensure this value is greater than or equal to",
    )

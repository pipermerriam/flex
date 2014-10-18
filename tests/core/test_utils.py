import six

from flex.utils import (
    is_non_string_iterable,
    is_value_of_type,
    format_errors,
)
from flex.constants import (
    NULL,
    BOOLEAN,
    INTEGER,
    NUMBER,
    STRING,
    ARRAY,
    OBJECT,
)


#
# is_non_string_iterable
#
def test_list():
    assert is_non_string_iterable([])


def test_dict():
    assert is_non_string_iterable({})


def test_tuple():
    assert is_non_string_iterable(tuple())


def test_not_string():
    assert not is_non_string_iterable('is-a-string')


#
# is_value_of_type
#
def test_null_type():
    assert is_value_of_type(None, NULL)


def test_non_null_type():
    assert not is_value_of_type(False, NULL)
    assert not is_value_of_type('', NULL)
    assert not is_value_of_type([], NULL)


def test_boolean_type():
    assert is_value_of_type(True, BOOLEAN)
    assert is_value_of_type(False, BOOLEAN)


def test_non_boolean_types():
    assert not is_value_of_type(None, BOOLEAN)
    assert not is_value_of_type('1', BOOLEAN)
    assert not is_value_of_type(1, BOOLEAN)
    assert not is_value_of_type('0', BOOLEAN)
    assert not is_value_of_type(0, BOOLEAN)
    assert not is_value_of_type([], BOOLEAN)


def test_integer_type():
    assert is_value_of_type(0, INTEGER)
    assert is_value_of_type(-1, INTEGER)
    assert is_value_of_type(1, INTEGER)


def test_non_integer_type():
    assert not is_value_of_type(1.0, INTEGER)
    assert not is_value_of_type(True, INTEGER)
    assert not is_value_of_type(False, INTEGER)


def test_number_type():
    assert is_value_of_type(0, NUMBER)
    assert is_value_of_type(1, NUMBER)
    assert is_value_of_type(1.0, NUMBER)


def test_non_number_types():
    assert not is_value_of_type('0', NUMBER)
    assert not is_value_of_type(True, NUMBER)
    assert not is_value_of_type([], NUMBER)


def test_string_type():
    assert is_value_of_type('', STRING)
    assert is_value_of_type(six.binary_type('string'), STRING)
    assert is_value_of_type(six.text_type('string'), STRING)


def test_non_string_type():
    assert not is_value_of_type(1, STRING)
    assert not is_value_of_type(True, STRING)
    assert not is_value_of_type(None, STRING)
    assert not is_value_of_type([], STRING)


def test_array_type():
    assert is_value_of_type([], ARRAY)
    assert is_value_of_type(tuple(), ARRAY)


def test_non_array_types():
    assert not is_value_of_type({}, ARRAY)
    assert not is_value_of_type(1, ARRAY)
    assert not is_value_of_type('1234', ARRAY)


def test_object_types():
    assert is_value_of_type({}, OBJECT)


def test_non_object_types():
    assert not is_value_of_type([], OBJECT)
    assert not is_value_of_type(tuple(), OBJECT)


#
# format_errors tests
#
def test_string():
    messages = list(format_errors("error"))

    assert messages == ["'error'"]


def test_short_iterable():
    input = ["error-a", "error-b"]
    expected = [
        "0. 'error-a'",
        "1. 'error-b'",
    ]
    actual = list(format_errors(input))

    assert set(actual) == set(expected)


def test_mapping_with_string_values():
    input = {
        'foo': 'bar',
        'bar': 'baz',
    }
    expected = [
        "'foo': 'bar'",
        "'bar': 'baz'",
    ]
    actual = list(format_errors(input))

    assert set(actual) == set(expected)


def test_mapping_with_iterables():
    input = {
        'foo': ['bar', 'baz'],
        'bar': ['baz', 'foo'],
    }
    expected = [
        "'foo':",
        "    0. 'bar'",
        "    1. 'baz'",
        "'bar':",
        "    0. 'baz'",
        "    1. 'foo'",
    ]
    actual = list(format_errors(input))

    assert set(actual) == set(expected)


def test_mapping_with_mappings():
    input = {
        'foo': {
            'bar': 'error-a',
            'baz': 'error-b',
        },
        'bar': {
            'baz': 'error-c',
            'foo': 'error-d',
        }
    }
    expected = [
        "'foo':",
        "    - 'bar': 'error-a'",
        "    - 'baz': 'error-b'",
        "'bar':",
        "    - 'baz': 'error-c'",
        "    - 'foo': 'error-d'",
    ]
    actual = list(format_errors(input))

    assert set(actual) == set(expected)


def test_iterable_of_mappings():
    input = [
        {'foo': 'bar'},
        {'bar': ['baz', 'foo']},
    ]
    expected = [
        "0. 'foo': 'bar'",
        "1. 'bar':",
        "    0. 'baz'",
        "    1. 'foo'",
    ]
    actual = list(format_errors(input))

    assert set(actual) == set(expected)

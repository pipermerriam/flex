import pytest

from flex.serializers.common import BaseParameterSerializer

from flex.constants import (
    PATH,
    BODY,
    QUERY,
    FORM_DATA,
    BOOLEAN,
    NUMBER,
    ARRAY,
    NULL,
    STRING,
    MULTI,
    HEADER,
)

from tests.utils import assert_error_message_equal


def test_parameter_in_path_but_missing_required():
    serializer = BaseParameterSerializer(
        data={'name': 'test', 'in': PATH}
    )

    assert not serializer.is_valid()
    assert 'required' in serializer.errors
    assert_error_message_equal(
        serializer.errors['required'][0],
        serializer.error_messages['path_parameters_are_required'],
    )


def test_parameter_in_path_but_declared_not_required():
    serializer = BaseParameterSerializer(
        data={'name': 'test', 'in': PATH, 'required': False}
    )

    assert not serializer.is_valid()
    assert 'required' in serializer.errors
    assert_error_message_equal(
        serializer.errors['required'][0],
        serializer.error_messages['path_parameters_are_required'],
    )


def test_parameter_in_path_with_required_truthy():
    serializer = BaseParameterSerializer(
        data={'name': 'test', 'in': PATH, 'required': True}
    )

    serializer.is_valid()
    assert 'required' not in serializer.errors


def assert_parameter_in_body_with_no_schema():
    serializer = BaseParameterSerializer(
        data={'name': 'test', 'in': BODY}
    )

    assert not serializer.is_valid()
    assert 'schema' in serializer.errors
    assert_error_message_equal(
        serializer.errors['schema'][0],
        serializer.error_messages['schema_required'],
    )


def assert_parameter_in_body_with_no_type():
    serializer = BaseParameterSerializer(
        data={'name': 'test', 'in': BODY}
    )

    assert not serializer.is_valid()
    assert 'type' in serializer.errors
    assert_error_message_equal(
        serializer.errors['type'][0],
        serializer.error_messages['type_required'],
    )


@pytest.mark.parametrize(
    'in_',
    (
        HEADER,
        PATH,
    )
)
def test_invalid_in_value_for_multi_collection_format(in_):
    serializer = BaseParameterSerializer(
        data={'name': 'test', 'in': in_, 'collectionFormat': MULTI}
    )

    assert not serializer.is_valid()
    assert 'collectionFormat' in serializer.errors
    assert_error_message_equal(
        serializer.errors['collectionFormat'][0],
        serializer.error_messages['collection_format_must_be_multi'],
    )


@pytest.mark.parametrize(
    'in_',
    (
        QUERY,
        FORM_DATA,
    )
)
def test_valid_in_values_for_multi_collection_format(in_):
    serializer = BaseParameterSerializer(
        data={'name': 'test', 'in': in_, 'collectionFormat': MULTI}
    )

    serializer.is_valid()
    assert 'collectionFormat' not in serializer.errors


@pytest.mark.parametrize(
    'type_,default',
    (
        (BOOLEAN, 'abc'),
        (BOOLEAN, 1),
        (NUMBER, True),
        (NUMBER, 'abc'),
        (ARRAY, 'abc'),
        (NULL, False),
        (STRING, 1),
        (STRING, None),
    )
)
def test_mistyped_parameter_default_boolean_to_string(type_, default):
    serializer = BaseParameterSerializer(
        data={'name': 'test', 'in': QUERY, 'type': type_, 'default': default}
    )

    assert not serializer.is_valid()
    assert 'default' in serializer.errors
    assert_error_message_equal(
        serializer.errors['default'][0],
        serializer.error_messages['default_is_incorrect_type'],
    )


def test_items_required_if_type_is_array():
    serializer = BaseParameterSerializer(
        data={'name': 'test', 'in': QUERY, 'type': ARRAY}
    )

    assert not serializer.is_valid()
    assert 'items' in serializer.errors
    assert_error_message_equal(
        serializer.errors['items'][0],
        serializer.error_messages['items_required'],
    )

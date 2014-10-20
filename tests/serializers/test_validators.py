from __future__ import unicode_literals
import pytest

import six

from rest_framework import serializers

from flex.serializers.validators import (
    host_validator,
    path_validator,
    scheme_validator,
    mimetype_validator,
    string_type_validator,
    type_validator,
    format_validator,
    parameter_in_validator,
    collection_format_validator,
    MinValueValidator,
    MaxValueValidator,
    security_type_validator,
    security_api_key_location_validator,
    security_flow_validator,
    regex_validator,
)
from flex.constants import (
    SCHEMES,
    MIMETYPES,
    FORMATS,
    PARAMETER_IN_VALUES,
    COLLECTION_FORMATS,
    NULL,
    INTEGER,
    SECURITY_TYPES,
    SECURITY_API_KEY_LOCATIONS,
    SECURITY_FLOWS,
)


#
# type_validator tests
#
def test_type_validator_accepts_lists_of_types():
    """
    Ensure that the `type` validator accepts an iterable of types.
    """
    type_validator([NULL, INTEGER])


def test_type_validator_accepts_single_type():
    """
    Ensure that the `type` validator accepts a singular type.
    """
    type_validator(INTEGER)


def test_invalid_singular_type():
    with pytest.raises(serializers.ValidationError):
        type_validator('not-a-real-type')


def test_invalid_type_in_iterable_of_types():
    with pytest.raises(serializers.ValidationError):
        value = [
            NULL,
            'not-a-real-type',
            INTEGER,
        ]
        type_validator(value)


#
# format_validator tests
#
def test_format_sanity_check():
    with pytest.raises(serializers.ValidationError):
        format_validator('not-a-real-format')


def test_valid_format():
    format_validator(FORMATS[0][1])


#
# string_type_validator tests
#
def test_raises_for_non_strings():
    """
    Mostly just sanity checking
    """
    with pytest.raises(serializers.ValidationError):
        string_type_validator(1)

    with pytest.raises(serializers.ValidationError):
        string_type_validator(None)


def test_accepts_iterables():
    string_type_validator(['test'])


def test_accepts_bytes():
    string_type_validator(six.binary_type('test'))


def test_accepts_unicode():
    string_type_validator(six.text_type('test'))


#
# mimetype_validator tests
#
def test_mimetype_invalid_value():
    with pytest.raises(serializers.ValidationError):
        mimetype_validator('not-a-real-mimetype')


def test_mimetype_singular_value():
    mimetype_validator(MIMETYPES[0])


def test_mimetype_iterable_value():
    mimetype_validator([MIMETYPES[0]])


#
# scheme_validator tests
#
def test_scheme_invalid_value():
    with pytest.raises(serializers.ValidationError):
        scheme_validator('not-a-real-scheme')


def test_scheme_singular_value():
    scheme_validator(SCHEMES[0])


def test_scheme_iterable_value():
    scheme_validator([SCHEMES[0]])


#
# path_validator tests
#
def test_no_leading_slash():
    """
    Must begin with a leading `/`
    """
    with pytest.raises(serializers.ValidationError):
        path_validator('no-leading/slash/')


def test_with_leading_slash():
    path_validator('/with-leading/slash/')


def test_with_non_path_component():
    """
    Invalid if it contains extra stuff that isn't part of the path.
    """
    with pytest.raises(serializers.ValidationError):
        path_validator('/no-leading/slash/?foo=3')


#
# host_validator tests
#
def test_invalid_with_scheme():
    with pytest.raises(serializers.ValidationError):
        host_validator('http://www.example.com')


def test_subdomain_host():
    host_validator('www.example.com')


def test_only_host():
    host_validator('example.com')


def test_valid_with_port():
    host_validator('example.com:8000')


#
# parameter_in_validator tests
#
def test_invalid_in_value():
    with pytest.raises(serializers.ValidationError):
        parameter_in_validator('not-a-valid-in-value')


def test_valid_in_value():
    parameter_in_validator(PARAMETER_IN_VALUES[0])


#
# collection_format_validator tests
#
def test_invalid_collection_format():
    with pytest.raises(serializers.ValidationError):
        collection_format_validator('not-a-valid-collection-format')


def test_valid_collection_format():
    collection_format_validator(COLLECTION_FORMATS[0])


#
# MinValueValidator tests
#

def test_inclusive_minimum():
    validator = MinValueValidator(5, allow_minimum=True)

    validator(5)
    validator(100)

    with pytest.raises(serializers.ValidationError):
        validator(4)


def test_exclusive_minimum():
    validator = MinValueValidator(5, allow_minimum=False)

    validator(6)
    validator(100)

    with pytest.raises(serializers.ValidationError):
        validator(5)


#
# MaxValueValidator tests
#
def test_inclusive_maximum():
    validator = MaxValueValidator(5, allow_maximum=True)

    validator(5)
    validator(0)

    with pytest.raises(serializers.ValidationError):
        validator(6)


def test_exclusive_maximum():
    validator = MaxValueValidator(5, allow_maximum=False)

    validator(4)
    validator(0)

    with pytest.raises(serializers.ValidationError):
        validator(5)


#
# security_type_validator tests
#
def test_unknown_security_type():
    with pytest.raises(serializers.ValidationError):
        security_type_validator('not-a-real-security-type')


def test_with_known_security_type():
    security_type_validator(SECURITY_TYPES[0])


#
# security_api_key_location_validator tests
#
def test_with_unkown_api_key_location():
    with pytest.raises(serializers.ValidationError):
        security_api_key_location_validator('not-a-real-security-api-key-location')


def test_with_known_api_key_location():
    security_api_key_location_validator(SECURITY_API_KEY_LOCATIONS[0])


#
# security_flow_validator tests
#
def test_with_unknown_flow():
    with pytest.raises(serializers.ValidationError):
        security_flow_validator('not-a-real-security-flow')


def test_with_known_flow():
    security_flow_validator(SECURITY_FLOWS[0])


#
# regex_validator
#
def test_with_invalid_regex():
    with pytest.raises(serializers.ValidationError):
        regex_validator('[abc')


def test_with_valid_regex():
    regex_validator('abc')

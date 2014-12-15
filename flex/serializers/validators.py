from __future__ import unicode_literals

import re
from six.moves import urllib_parse as urlparse
import operator

import six

from django.core.validators import RegexValidator

from flex.exceptions import ValidationError
from flex.formats import registry
from flex.decorators import (
    maybe_iterable,
    translate_validation_error,
)
from flex.utils import is_value_of_type
from flex.constants import (
    SCHEMES,
    PRIMATIVE_TYPES,
    PARAMETER_IN_VALUES,
    COLLECTION_FORMATS,
    HEADER_TYPES,
    SECURITY_TYPES,
    SECURITY_API_KEY_LOCATIONS,
    SECURITY_FLOWS,
    ARRAY,
)
from flex.error_messages import MESSAGES


def host_validator(value):
    parts = urlparse.urlparse(value)
    host = parts.netloc or parts.path
    if value != host:
        raise ValidationError(
            "Invalid host: {0}, expected {1}".format(value, host),
        )


def path_validator(value):
    if not value.startswith('/'):
        raise ValidationError("Path must start with a '/'")
    parts = urlparse.urlparse(value)
    if value != parts.path:
        raise ValidationError("Invalid Path: {0}".format(value))


@maybe_iterable
def scheme_validator(value):
    if value not in SCHEMES:
        raise ValidationError("Unknown scheme: {0}".format(value))


# top-level type name / [ tree. ] subtype name [ +suffix ] [ ; parameters ]

TOP_LEVEL_TYPE_NAMES = set((
    'application',
    'audio',
    'example',
    'image',
    'message',
    'model',
    'multipart',
    'text',
    'video',
))


MIMETYPE_PATTERN = (
    '^'
    '(application|audio|example|image|message|model|multipart|text|video)'  # top-level type name
    '/'
    '(vnd(\.[-a-zA-Z0-9]+)*\.)?'  # vendor tree
    '([-a-zA-Z0-9]+)'  # media type
    '(\+(xml|json|ber|der|fastinfoset|wbxml|zip))?'
    '((; [-a-zA-Z0-9]+=(([-\.a-zA-Z0-9]+)|(("|\')[-\.a-zA-Z0-9]+("|\'))))+)?'  # parameters
    '$'
)


@maybe_iterable
def mimetype_validator(value):
    return translate_validation_error(RegexValidator(MIMETYPE_PATTERN).__call__)(value)


@maybe_iterable
def string_type_validator(value):
    if not isinstance(value, (six.binary_type, six.text_type)):
        raise ValidationError("Must be a string")


def format_validator(value):
    if value not in registry.formats:
        # TODO: unknown formats are ok, but want to be sure we have all of the
        # common ones before removing this.
        raise ValidationError('Unknown format: {0}'.format(value))


@maybe_iterable
def type_validator(value):
    if value not in PRIMATIVE_TYPES:
        raise ValidationError(MESSAGES['type']['unknown'].format(value))


def header_type_validator(value):
    if value not in HEADER_TYPES:
        raise ValidationError(
            MESSAGES['type']['invalid_header_type'].format(value),
        )


def parameter_in_validator(value):
    if value not in PARAMETER_IN_VALUES:
        raise ValidationError(
            "Unknown value for in: `{0}`".format(value),
        )


def collection_format_validator(value):
    if value not in COLLECTION_FORMATS:
        raise ValidationError(
            "Unknown collectionFormat: `{0}`".format(value),
        )


def MinValueValidator(minimum, allow_minimum=False):
    def validator(value):
        if allow_minimum:
            op = operator.ge
            msg_txt = "greater than or equal to"
        else:
            op = operator.gt
            msg_txt = "greater than"
        if not op(value, minimum):
            raise ValidationError(
                "{0} is not {1} `{2}`".format(
                    value, msg_txt, minimum,
                ),
            )

    return validator


def MaxValueValidator(maximum, allow_maximum=False):
    def validator(value):
        if allow_maximum:
            op = operator.le
            msg_txt = "less than or equal to"
        else:
            op = operator.lt
            msg_txt = "less than"
        if not op(value, maximum):
            raise ValidationError(
                "{0} is not {1} `{2}`".format(
                    value, msg_txt, maximum,
                ),
            )

    return validator


def security_type_validator(value):
    if value not in SECURITY_TYPES:
        raise ValidationError(
            "Unknown security type: {0}".format(value),
        )


def security_api_key_location_validator(value):
    if value not in SECURITY_API_KEY_LOCATIONS:
        raise ValidationError(
            "Unknown api key location: {0}".format(value),
        )


def security_flow_validator(value):
    if value not in SECURITY_FLOWS:
        raise ValidationError(
            "Unknown security flow: {0}".format(value),
        )


def regex_validator(value):
    try:
        re.compile(value)
    except re.error as e:
        raise ValidationError(
            "Invalid Regex: {0}".format(str(e))
        )


def is_array_validator(value):
    if not is_value_of_type(value, ARRAY):
        raise ValidationError(
            "Must be an array",
        )

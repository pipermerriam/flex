import itertools
import pytest

from flex.loading.schema import (
    mimetype_validator,
)
from flex.loading.schema.host import decompose_hostname
from flex.exceptions import ValidationError
from flex.error_messages import MESSAGES

from tests.utils import (
    assert_message_in_errors,
    assert_path_not_in_errors,
    assert_path_in_errors,
)


@pytest.mark.parametrize(
    'value',
    ('application/json', 1, 1.1, {'a': 1}, None),
)
def test_mimetype_invalid_for_non_array_value(value):
    with pytest.raises(ValidationError) as err:
        mimetype_validator(value)

    assert_message_in_errors(
        MESSAGES['type']['invalid'],
        err.value.detail,
        'type',
    )


@pytest.mark.parametrize(
    'value',
    (
        ['application/json'],
        ['application/json'],
        ['image/svg+xml'],
        ['application/vnd.oasis.opendocument.text'],
        ['text/plain; charset=utf-8'],
        ['video/mp4'],
        ['video/mp4; codecs="avc1.640028"'],
        ["video/mp4; codecs='avc1.640028'"],
        ['application/xhtml+xml'],
        ['image/png'],
        ['application/vnd.ms-excel'],
    )
)
def test_mimetype_with_valid_values(value):
    try:
        mimetype_validator(value)
    except ValidationError as err:
        errors = err.detail
    else:
        errors = {}

    assert_path_not_in_errors(
        'type',
        errors,
    )
    assert_path_not_in_errors(
        'value',
        errors,
    )


@pytest.mark.parametrize(
    'value',
    (
        ['invalidtypename/json'],
        ['noslash'],
    )
)
def test_mimetype_with_invalid_values(value):
    with pytest.raises(ValidationError) as err:
        mimetype_validator(value)

    assert_message_in_errors(
        MESSAGES['mimetype']['invalid'],
        err.value.detail,
        'value',
    )


def test_mimetype_with_multiple_valid_values():
    try:
        mimetype_validator(['application/json', 'application/xml'])
    except ValidationError as err:
        errors = err.detail
    else:
        errors = {}

    assert_path_not_in_errors(
        'type',
        errors,
    )
    assert_path_not_in_errors(
        'value',
        errors,
    )


def test_mimetype_with_invalid_value_in_multiple_values():
    with pytest.raises(ValidationError) as err:
        mimetype_validator(['application/json', 'not-a-valid-mimetype'])

    assert_message_in_errors(
        MESSAGES['mimetype']['invalid'],
        err.value.detail,
        'value',
    )

import pytest

from flex.loading.schema import (
    info_validator,
    swagger_schema_validator,
)
from flex.exceptions import ValidationError
from flex.error_messages import MESSAGES

from tests.utils import (
    assert_message_in_errors,
    assert_path_not_in_errors,
)
from tests.factories import (
    RawSchemaFactory,
)


NON_STRING_VALUES = (1, 1.1, True, ['a', 'b'], {'a': 'b'}, None)


def test_info_field_is_required():
    """
    Test that the info field is required for overall schema validation.
    """
    raw_schema = RawSchemaFactory()
    raw_schema.pop('info', None)

    assert 'info' not in raw_schema

    with pytest.raises(ValidationError) as err:
        swagger_schema_validator(raw_schema)

    assert_message_in_errors(
        MESSAGES['required']['required'],
        err.value.detail,
        'required.info',
    )


#
# title
#
def test_title_is_required():
    data = {}
    with pytest.raises(ValidationError) as err:
        info_validator(data)

    assert_message_in_errors(
        MESSAGES['required']['required'],
        err.value.detail,
        'required.title',
    )


@pytest.mark.parametrize(
    'value',
    NON_STRING_VALUES,
)
def test_title_type_must_be_string(value):
    data = {
        'title': value,
    }
    with pytest.raises(ValidationError) as err:
        info_validator(data)

    assert_message_in_errors(
        MESSAGES['type']['invalid'],
        err.value.detail,
        'title.type',
    )


#
# description
#
def test_description_is_not_required():
    data = {}
    try:
        info_validator(data)
    except ValidationError as err:
        errors = err.detail
    else:
        errors = {}

    assert_path_not_in_errors(
        'description.required',
        errors,
    )


@pytest.mark.parametrize(
    'value',
    NON_STRING_VALUES,
)
def test_description_must_be_a_string(value):
    data = {
        'description': value,
    }
    with pytest.raises(ValidationError) as err:
        info_validator(data)

    assert_message_in_errors(
        MESSAGES['type']['invalid'],
        err.value.detail,
        'description.type',
    )


#
# termsOfService
#
def test_terms_of_service_is_not_required():
    data = {}
    try:
        info_validator(data)
    except ValidationError as err:
        errors = err.detail
    else:
        errors = {}

    assert_path_not_in_errors(
        'termsOfService.required',
        errors,
    )


@pytest.mark.parametrize(
    'value',
    NON_STRING_VALUES,
)
def test_terms_of_service_must_be_a_string(value):
    data = {
        'termsOfService': value,
    }
    with pytest.raises(ValidationError) as err:
        info_validator(data)

    assert_message_in_errors(
        MESSAGES['type']['invalid'],
        err.value.detail,
        'termsOfService.type',
    )


#
# contact
#
def test_contact_is_not_required():
    data = {}
    try:
        info_validator(data)
    except ValidationError as err:
        errors = err.detail
    else:
        errors = {}

    assert_path_not_in_errors(
        'contact.required',
        errors,
    )


@pytest.mark.parametrize(
    'value',
    ('abc', 1, 2.2, ['a', 'b'], None, True),
)
def test_contact_must_be_an_object(value):
    data = {
        'contact': value,
    }
    with pytest.raises(ValidationError) as err:
        info_validator(data)

    assert_message_in_errors(
        MESSAGES['type']['invalid'],
        err.value.detail,
        'contact.type',
    )


#
# contact.name
#
@pytest.mark.parametrize(
    'value',
    NON_STRING_VALUES,
)
def test_contact_object_name_type_validation(value):
    data = {
        'contact': {'name': value},
    }
    with pytest.raises(ValidationError) as err:
        info_validator(data)

    assert_message_in_errors(
        MESSAGES['type']['invalid'],
        err.value.detail,
        'contact.name.type',
    )


def test_contact_object_name_with_good_value():
    data = {
        'contact': {'name': 'Test Name'},
    }
    try:
        info_validator(data)
    except ValidationError as err:
        errors = err.detail
    else:
        errors = {}

    assert_path_not_in_errors(
        'contact.name',
        errors,
    )


#
# contact.email
#
@pytest.mark.parametrize(
    'value',
    NON_STRING_VALUES,
)
def test_contact_object_email_type_validation(value):
    data = {
        'contact': {'email': value},
    }
    with pytest.raises(ValidationError) as err:
        info_validator(data)

    assert_message_in_errors(
        MESSAGES['type']['invalid'],
        err.value.detail,
        'contact.email.type',
    )


def test_contact_object_email_format_validation():
    data = {
        'contact': {'email': 'not-a-valid-email'},
    }
    with pytest.raises(ValidationError) as err:
        info_validator(data)

    assert_message_in_errors(
        MESSAGES['format']['invalid_email'],
        err.value.detail,
        'contact.email.format',
    )


def test_contact_object_email_with_good_value():
    data = {
        'contact': {'email': 'test@example.com'},
    }
    try:
        info_validator(data)
    except ValidationError as err:
        errors = err.detail
    else:
        errors = {}

    assert_path_not_in_errors(
        'contact.email',
        errors,
    )


#
# contact.url
#
@pytest.mark.parametrize(
    'value',
    NON_STRING_VALUES,
)
def test_contact_object_url_type_validation(value):
    data = {
        'contact': {'url': value},
    }
    with pytest.raises(ValidationError) as err:
        info_validator(data)

    assert_message_in_errors(
        MESSAGES['type']['invalid'],
        err.value.detail,
        'contact.url.type',
    )


def test_contact_object_url_format_validation():
    data = {
        'contact': {'url': 'not-a-valid-url'},
    }
    with pytest.raises(ValidationError) as err:
        info_validator(data)

    assert_message_in_errors(
        MESSAGES['format']['invalid_uri'],
        err.value.detail,
        'contact.url.format',
    )


def test_contact_object_url_with_good_value():
    data = {
        'contact': {'url': 'http://www.example.com'},
    }
    try:
        info_validator(data)
    except ValidationError as err:
        errors = err.detail
    else:
        errors = {}

    assert_path_not_in_errors(
        'contact.url',
        errors,
    )


#
# license
#
def test_license_is_not_required():
    data = {}
    try:
        info_validator(data)
    except ValidationError as err:
        errors = err.detail
    else:
        errors = {}

    assert_path_not_in_errors(
        'license.required',
        errors,
    )


@pytest.mark.parametrize(
    'value',
    ('abc', 1, 2.2, ['a', 'b'], None, True),
)
def test_license_must_be_an_object(value):
    data = {
        'license': value,
    }
    with pytest.raises(ValidationError) as err:
        info_validator(data)

    assert_message_in_errors(
        MESSAGES['type']['invalid'],
        err.value.detail,
        'license.type',
    )


#
# license.name
#
@pytest.mark.parametrize(
    'value',
    NON_STRING_VALUES,
)
def test_license_name_must_be_a_string(value):
    data = {
        'license': {
            'name': value,
        },
    }
    with pytest.raises(ValidationError) as err:
        info_validator(data)

    assert_message_in_errors(
        MESSAGES['type']['invalid'],
        err.value.detail,
        'license.name.type',
    )


def test_license_name_with_good_value():
    data = {
        'license': {
            'name': 'MIT',
        },
    }
    try:
        info_validator(data)
    except ValidationError as err:
        errors = err.detail
    else:
        errors = {}

    assert_path_not_in_errors(
        'license.name',
        errors,
    )


#
# license.url
#
@pytest.mark.parametrize(
    'value',
    NON_STRING_VALUES,
)
def test_license_url_must_be_a_string(value):
    data = {
        'license': {
            'url': value,
        },
    }
    with pytest.raises(ValidationError) as err:
        info_validator(data)

    assert_message_in_errors(
        MESSAGES['type']['invalid'],
        err.value.detail,
        'license.url.type',
    )


def test_license_url_must_be_valid_url():
    data = {
        'license': {
            'url': 'not-a-valid-url',
        },
    }
    with pytest.raises(ValidationError) as err:
        info_validator(data)

    assert_message_in_errors(
        MESSAGES['format']['invalid_uri'],
        err.value.detail,
        'license.url.format',
    )


def test_license_url_with_good_value():
    data = {
        'license': {
            'url': 'http://www.example.com',
        },
    }
    try:
        info_validator(data)
    except ValidationError as err:
        errors = err.detail
    else:
        errors = {}

    assert_path_not_in_errors(
        'license.url',
        errors,
    )


#
# version
#
def test_version_is_not_required():
    data = {}
    try:
        info_validator(data)
    except ValidationError as err:
        errors = err.detail
    else:
        errors = {}

    assert_path_not_in_errors(
        'version.required',
        errors,
    )


@pytest.mark.parametrize(
    'value',
    NON_STRING_VALUES,
)
def test_version_must_be_a_string(value):
    data = {
        'version': value,
    }
    with pytest.raises(ValidationError) as err:
        info_validator(data)

    assert_message_in_errors(
        MESSAGES['type']['invalid'],
        err.value.detail,
        'version.type',
    )

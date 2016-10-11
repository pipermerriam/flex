import os.path

import pytest

from flex.constants import (
    STRING,
)
from flex.error_messages import MESSAGES
from flex.exceptions import ValidationError

from tests.utils import (
    assert_message_in_errors,
    assert_path_not_in_errors,
)

from flex.loading.common.reference import (
    reference_object_validator,
)


DIR = os.path.dirname(os.path.abspath(__file__))


def test_ref_is_required():
    ref_schema = {}

    with pytest.raises(ValidationError) as err:
        reference_object_validator(ref_schema)

    assert_message_in_errors(
        MESSAGES['required']['required'],
        err.value.detail,
        'required.$ref',
    )


@pytest.mark.parametrize(
    'value',
    ({'a': 'abc'}, 1, 1.1, True, ['a', 'b'], None),
)
def test_ref_with_invalid_types(value):
    schema = {'$ref': value}

    with pytest.raises(ValidationError) as err:
        reference_object_validator(schema)

    assert_message_in_errors(
        MESSAGES['type']['invalid'],
        err.value.detail,
        '$ref.type',
    )


def test_valid_reference():
    schema = {'$ref': '#/definitions/SomeReference'}
    context = {
        'definitions': {
            'SomeReference': {
                'type': STRING,
            }
        }
    }

    try:
        reference_object_validator(schema, context=context)
    except ValidationError as err:
        errors = err.detail
    else:
        errors = {}

    assert_path_not_in_errors(
        '$ref',
        errors,
    )


def test_external_relative_reference():
    schema = {'$ref': 'reference_schemas/ext_relative.json#'}

    try:
        reference_object_validator(schema, context={}, base_path=DIR)
    except ValidationError as err:
        errors = err.detail
    else:
        errors = {}

    assert_path_not_in_errors(
        '$ref',
        errors,
    )


def test_external_absolute_reference():
    absolute_path = os.path.join(DIR, 'reference_schemas/ext_relative.json')
    schema = {'$ref': '{}#'.format(absolute_path)}

    try:
        reference_object_validator(schema, context={})
    except ValidationError as err:
        errors = err.detail
    else:
        errors = {}

    assert_path_not_in_errors(
        '$ref',
        errors,
    )

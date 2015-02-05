import pytest

from flex.error_messages import MESSAGES
from flex.exceptions import ValidationError
from flex.loading.schema.paths.path_item.operation.responses.single.schema import (
    schema_validator,
)


def test_context_missing_definitions(msg_assertions):
    with pytest.raises(KeyError) as err:
        schema_validator({'$ref': 'SomeReference'})

    msg_assertions.assert_error_message_equal(
        str(err.value),
        MESSAGES['unknown_reference']['no_definitions'],
    )


def test_reference_not_found_in_definitions(msg_assertions):
    with pytest.raises(ValidationError) as err:
        schema_validator({'$ref': 'UnknownReference'}, context={'definitions': set()})

    msg_assertions.assert_message_in_errors(
        MESSAGES['unknown_reference']['definition'],
        err.value.detail,
        '$ref',
    )


def test_with_valid_reference(msg_assertions):
    try:
        schema_validator({'$ref': 'SomeReference'}, context={'definitions': {'SomeReference'}})
    except ValidationError as err:
        errors = err.detail
    else:
        errors = {}

    msg_assertions.assert_path_not_in_errors(
        '$ref', errors,
    )


@pytest.mark.parametrize(
    'value',
    (1, 1.1, True, None, ['a', 'b'], {'a': 'b'}),
)
def test_reference_type_validation(value, msg_assertions):
    with pytest.raises(ValidationError) as err:
        schema_validator({'$ref': value})

    msg_assertions.assert_message_in_errors(
        MESSAGES['type']['invalid'],
        err.value.detail,
        '$ref',
    )

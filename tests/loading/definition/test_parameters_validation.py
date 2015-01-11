import pytest

from flex.error_messages import MESSAGES
from flex.exceptions import ValidationError
from flex.loading.definition import (
    definitions_validator,
)

from tests.utils import (
    assert_path_not_in_errors,
    assert_message_in_errors,
)


def test_parameters_definitions_are_not_required():
    context = {'deferred_references': set()}
    try:
        definitions_validator({}, context=context)
    except ValidationError as err:
        errors = err.detail
    else:
        errors = {}

    assert_path_not_in_errors(
        'parameters',
        errors,
    )


@pytest.mark.parametrize(
    'value',
    ('abc', 1, 1.1, True, None, {'a': 1}),
)
def test_parameters_definitions_type_validation_for_invalid_types(value):
    context = {'deferred_references': set()}
    with pytest.raises(ValidationError) as err:
        definitions_validator({'parameters': value}, context=context)

    assert_message_in_errors(
        MESSAGES['type']['invalid'],
        err.value.detail,
        'parameters',
    )

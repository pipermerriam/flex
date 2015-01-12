import pytest

from flex.error_messages import MESSAGES
from flex.exceptions import ValidationError
from flex.loading.definitions.parameters import (
    single_parameter_validator,
)

from tests.utils import (
    assert_path_not_in_errors,
    assert_message_in_errors,
)


def test_name_is_required():
    context = {'deferred_references': set()}
    with pytest.raises(ValidationError) as err:
        single_parameter_validator({}, context=context)

    assert_message_in_errors(
        MESSAGES['required']['required'],
        err.value.detail,
        'name',
    )


def test_in_is_required():
    context = {'deferred_references': set()}
    with pytest.raises(ValidationError) as err:
        single_parameter_validator({}, context=context)

    assert_message_in_errors(
        MESSAGES['required']['required'],
        err.value.detail,
        'in',
    )

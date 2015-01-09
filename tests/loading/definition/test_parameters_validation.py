from flex.exceptions import ValidationError
from flex.loading.definition import (
    definitions_validator,
)

from tests.utils import (
    assert_path_not_in_errors,
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

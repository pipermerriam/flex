import pytest

from flex.constants import EMPTY

from tests.utils import generate_validator_from_schema


def test_field_declared_as_required():
    schema = {
        'required': True,
    }
    validator = generate_validator_from_schema(schema)

    with pytest.raises(ValueError):
        validator(EMPTY)


def test_field_declared_as_required_with_field_present_is_valid():
    schema = {
        'required': True,
    }
    validator = generate_validator_from_schema(schema)

    validator('John Smith')

import pytest

from tests.utils import generate_validator_from_schema


def test_field_declared_as_required():
    schema = {
        'name': {
            'required': True,
        },
    }
    validator = generate_validator_from_schema(schema)

    with pytest.raises(ValueError):
        validator({})


def test_field_declared_as_required_with_field_present_is_valid():
    schema = {
        'name': {
            'required': True,
        },
    }
    validator = generate_validator_from_schema(schema)

    validator({'name': 'John Smith'})

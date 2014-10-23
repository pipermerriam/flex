import pytest

from flex.serializers.definitions import DefinitionsSerializer
from flex.constants import STRING

from tests.utils import generate_validator_from_schema


#
# reference validation tests
#
@pytest.mark.parametrize(
    'zipcode',
    (
        '80205',
        '80205-1234',
        '80205 1234',
    ),
)
def test_reference_with_valid_values(zipcode):
    schema = {
        'zipcode': {
            '$ref': 'ZipCode',
        },
    }
    context = {
        'definitions': {
            'ZipCode': {
                'type': STRING,
                'minLength': 5,
                'maxLength': 10,
            },
        },
    }
    validator = generate_validator_from_schema(schema, context=context)

    validator({'zipcode': zipcode})


@pytest.mark.parametrize(
    'zipcode',
    (
        '8020',  # too short
        80205,  # not a string
        '80205-12345', # too long
    ),
)
def test_reference_with_invalid_values(zipcode):
    schema = {
        'zipcode': {
            '$ref': 'ZipCode',
        },
    }
    context = {
        'definitions': {
            'ZipCode': {
                'type': STRING,
                'minLength': 5,
                'maxLength': 10,
            },
        },
    }
    validator = generate_validator_from_schema(schema, context=context)

    with pytest.raises(ValueError):
        validator({'zipcode': zipcode})


@pytest.mark.parametrize(
    'name',
    (
        'Piper',
        'Matthew',
        'Lindsey',
        'Lynn',
    ),
)
def test_reference_with_additional_validators_and_valid_value(name):
    schema = {
        'name': {
            '$ref': 'Name',
            'pattern': '^[A-Z][a-z]*$',
        },
    }
    context = {
        'definitions': {
            'Name': {
                'type': STRING,
                'minLength': 4,
                'maxLength': 7,
            },
        },
    }
    validator = generate_validator_from_schema(schema, context=context)

    validator({'name': name})


@pytest.mark.parametrize(
    'name',
    (
        'Joe', # too short
        'piper',  # not capitalized
        'Jennifer',  # too long
    ),
)
def test_reference_with_additional_validators_and_invalid_value(name):
    schema = {
        'name': {
            '$ref': 'Name',
            'pattern': '^[A-Z][a-z]*$',
        },
    }
    context = {
        'definitions': {
            'Name': {
                'type': STRING,
                'minLength': 4,
                'maxLength': 7,
            },
        },
    }
    validator = generate_validator_from_schema(schema, context=context)

    with pytest.raises(ValueError):
        validator({'name': name})


def test_circular_reference():
    schema = {
        'parent': {'$ref': 'Node'},
    }
    serializer = DefinitionsSerializer(
        data={
            'Node': {
                'properties': {
                    'parent': {'$ref': 'Node'},
                    'value': {'type': STRING},
                },
            },
        },
        context={'deferred_references': set()},
    )
    assert serializer.is_valid(), serializer.errors
    definitions = serializer.object

    validator = generate_validator_from_schema(
        schema,
        context={'definitions': definitions},
    )

    validator({
        'parent': {
            'value': 'bar',
            'parent': {
                'value': 1234,
                'parent': {
                    'value': 'baz',
                    'parent': {
                        'value': 54321,
                    },
                },
            },
        },
    })

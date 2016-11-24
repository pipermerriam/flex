import os.path

import pytest

from flex.exceptions import ValidationError
from flex.error_messages import MESSAGES
from flex.constants import (
    OBJECT,
    STRING,
)
from flex.loading.definitions import (
    definitions_validator,
)
from tests.utils import (
    assert_message_in_errors,
)


DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_references_end_up_in_deferred_referrences():
    deferred_references = set()
    context = {'deferred_references': deferred_references}

    definitions = {
        'definitions': {
            'SomeReference': {
                'type': OBJECT,
                'properties': {
                    'address': {
                        '$ref': '#/definitions/Address',
                    }
                }
            },
            'Address': {
                'type': STRING,
            }
        }
    }
    definitions_validator(definitions, context=context)
    assert '#/definitions/Address' in deferred_references


def test_deferred_references_are_validated():
    deferred_references = set()
    context = {'deferred_references': deferred_references}

    definitions = {
        'definitions': {
            'SomeReference': {
                'type': OBJECT,
                'properties': {
                    'address': {
                        '$ref': '#/definitions/Address',
                    }
                }
            },
        }
    }
    with pytest.raises(ValidationError) as err:
        definitions_validator(definitions, context=context)

    assert_message_in_errors(
        MESSAGES['reference']['undefined'],
        err.value.detail,
        'definitions.Address',
    )


def test_references_end_up_in_external_deferred_references():
    deferred_references = set()
    context = {'deferred_references': deferred_references}

    definitions = {
        'definitions': {
            'SomeReference': {
                'type': OBJECT,
                'properties': {
                    'address': {
                        '$ref': 'jsonschemas/ext.json#',
                    }
                }
            },
            'Address': {
                'type': STRING,
            }
        }
    }
    definitions_validator(definitions, context=context, base_path=DIR)
    assert 'jsonschemas/ext.json#' in deferred_references

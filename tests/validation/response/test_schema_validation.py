import json
import pytest

from flex.constants import (
    INTEGER,
)
from flex.validation.response import (
    generate_response_validator,
)
from flex.error_messages import MESSAGES

from tests.factories import (
    SchemaFactory,
    ResponseFactory,
)
from tests.utils import assert_error_message_equal


def test_basic_response_body_schema_validation_with_invalid_value():
    from django.core.exceptions import ValidationError
    schema = SchemaFactory(
        paths={
            '/get': {
                'get': {
                    'responses': {
                        200: {
                            'description': 'Success',
                            'schema': {'type': INTEGER},
                        }
                    },
                },
            },
        },
    )
    response_validator = generate_response_validator(schema, inner=True)

    response = ResponseFactory(
        url='http://www.example.com/get',
        status_code=200,
        content_type='application/json',
        content=json.dumps('not-an-integer'),
    )

    with pytest.raises(ValidationError) as err:
        response_validator(response)

    assert 'response_body' in err.value.messages[0]
    assert 'type' in err.value.messages[0]['response_body'][0]
    assert_error_message_equal(
        err.value.messages[0]['response_body'][0]['type'][0],
        MESSAGES['type']['invalid'],
    )

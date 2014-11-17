import pytest

from flex.validation.request import (
    validate_request,
)
from flex.error_messages import MESSAGES
from flex.constants import (
    INTEGER,
    HEADER,
    ARRAY,
    CSV,
    SSV,
    TSV,
    PIPES,
)

from tests.factories import (
    SchemaFactory,
    RequestFactory,
)
from tests.utils import assert_error_message_equal


def test_request_header_validation():
    from django.core.exceptions import ValidationError

    schema = SchemaFactory(
        paths={
            '/get/': {
                'get': {
                    'responses': {200: {'description': "Success"}},
                    'parameters': [
                        {
                            'name': 'Authorization',
                            'in': HEADER,
                            'type': INTEGER,
                        }
                    ]
                },
            },
        },
    )

    request = RequestFactory(
        url='http://www.example.com/get/',
        headers={'Authorization': 'abc'},
    )

    with pytest.raises(ValidationError) as err:
        validate_request(
            request,
            paths=schema['paths'],
            base_path=schema.get('base_path', ''),
            context=schema,
            inner=True,
        )

    assert 'method' in err.value.messages[0]
    assert 'parameters' in err.value.messages[0]['method'][0][0]
    assert 'headers' in err.value.messages[0]['method'][0][0]['parameters'][0]
    assert 'Authorization' in err.value.messages[0]['method'][0][0]['parameters'][0]['headers'][0]
    assert 'type' in err.value.messages[0]['method'][0][0]['parameters'][0]['headers'][0]['Authorization'][0]
    assert_error_message_equal(
        err.value.messages[0]['method'][0][0]['parameters'][0]['headers'][0]['Authorization'][0]['type'][0],
        MESSAGES['type']['invalid'],
    )


@pytest.mark.parametrize(
    'format_,value',
    (
        (CSV, '1,2,3'),
        (SSV, '1 2 3'),
        (TSV, '1\t2\t3'),
        (PIPES, '1|2|3'),
    ),
)
def test_request_header_array_extraction(format_, value):
    schema = SchemaFactory(
        paths={
            '/get/': {
                'get': {
                    'responses': {200: {'description': "Success"}},
                    'parameters': [
                        {
                            'name': 'Authorization',
                            'in': HEADER,
                            'type': ARRAY,
                            'collectionFormat': format_,
                            'minItems': 3,
                            'maxItems': 3,
                            'items': {
                                'type': INTEGER,
                                'minimum': 1,
                                'maximum': 3,
                            },
                        },
                    ],
                },
            },
        },
    )

    response = RequestFactory(
        url='http://www.example.com/get/',
        headers={'Authorization': value},
    )

    validate_request(
        response,
        paths=schema['paths'],
        base_path=schema.get('base_path', ''),
        context=schema,
    )

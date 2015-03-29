import pytest
import json

from flex.constants import EMPTY

from tests.factories import (
    RequestFactory,
)

def test_null_body_returns_null():
    request = RequestFactory(body=None)
    assert request.data is None


def test_empty_string_body_returns_empty_string():
    request = RequestFactory(body='')
    assert request.data == ''


def test_empty_body_returns_empty():
    request = RequestFactory(body=EMPTY)
    assert request.data is EMPTY


def test_json_content_type_with_json_body():
    request = RequestFactory(
        body=json.dumps({'key': 'value'}),
        content_type='application/json',
    )
    assert request.data == {'key': 'value'}


def test_unsupported_content_type():
    request = RequestFactory(
        body=json.dumps({'key': 'value'}),
        content_type='application/unsupported',
    )
    with pytest.raises(NotImplementedError):
        request.data

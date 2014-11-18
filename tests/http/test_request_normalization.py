import pytest
import urllib

import six

import requests

from flex.http import (
    normalize_request,
)


#
#  Test normalizatin of the request object from the requests library
#
def test_request_normalization(httpbin):
    raw_response = requests.post(httpbin.url + '/post')

    request = normalize_request(raw_response.request)

    assert request.path == '/post'
    assert request.content_type is None
    assert request.url == httpbin.url + '/post'
    assert request.method == 'post'


def test_request_normalization_with_content_type(httpbin):
    raw_response = requests.post(
        httpbin.url + '/post',
        headers={'Content-Type': 'application/json'},
    )

    request = normalize_request(raw_response.request)

    assert request.path == '/post'
    assert request.content_type == 'application/json'
    assert request.url == httpbin.url + '/post'
    assert request.method == 'post'


#
# Test urllib request object
#
@pytest.mark.skipif(six.PY3, reason="No urllib2 in python3")
def test_python2_urllib_request_normalization(httpbin):
    import urllib2

    raw_request = urllib2.Request(
        httpbin.url + '/get',
        headers={'Content-Type': 'application/json'},
    )

    request = normalize_request(raw_request)

    assert request.path == '/get'
    assert request.content_type == 'application/json'
    assert request.url == httpbin.url + '/get'
    assert request.method == 'get'


@pytest.mark.skipif(six.PY2, reason="No urllib3 in python2")
def test_python3_urllib_request_normalization(httpbin):
    raw_request = urllib.request.Request(
        httpbin.url + '/get',
        headers={'Content-Type': 'application/json'},
    )

    request = normalize_request(raw_request)

    assert request.path == '/get'
    assert request.content_type == 'application/json'
    assert request.url == httpbin.url + '/get'
    assert request.method == 'get'

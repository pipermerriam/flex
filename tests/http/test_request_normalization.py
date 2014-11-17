import urllib
import urllib2

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
def test_urllib_request_normalization(httpbin):
    raw_request = urllib2.Request(
        httpbin.url + '/get',
        headers={'Content-Type': 'application/json'},
    )

    request = normalize_request(raw_request)

    assert request.path == '/get'
    assert request.content_type == 'application/json'
    assert request.url == httpbin.url + '/get'
    assert request.method == 'get'

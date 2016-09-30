import pytest
import urllib

import six

import requests

from flex.http import (
    normalize_request, _tornado_available, _falcon_available
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


#
# Test tornado request object
#
@pytest.mark.skipif(not _tornado_available, reason="tornado not installed")
def test_tornado_client_request_normalization(httpbin):
    import tornado.httpclient

    raw_request = tornado.httpclient.HTTPRequest(
        httpbin.url + '/get?key=val',
        headers={'Content-Type': 'application/json'}
    )

    request = normalize_request(raw_request)

    assert request.path == '/get'
    assert request.content_type == 'application/json'
    assert request.url == httpbin.url + '/get?key=val'
    assert request.method == 'get'


@pytest.mark.skipif(not _tornado_available, reason="tornado not installed")
def test_tornado_server_request_normalization(httpbin):
    import tornado.httpserver

    raw_request = tornado.httpserver.HTTPRequest(
        'GET',
        httpbin.url + '/get?key=val',
        headers={'Content-Type': 'application/json'}
    )

    request = normalize_request(raw_request)

    assert request.path == '/get'
    assert request.content_type == 'application/json'
    assert request.url == httpbin.url + '/get?key=val'
    assert request.method == 'get'


@pytest.mark.skipif(not _falcon_available, reason="falcon not installed")
def test_falcon_request_normalization(httpbin):
    import falcon
    from falcon.testing.helpers import create_environ

    env = create_environ(
        path='/put',
        query_string='key=val',
        host=httpbin.host,
        port=httpbin.port,
        headers={'Content-Type': 'application/json'},
        body=b'{"key2": "val2"}',
        method='PUT',
    )
    raw_request = falcon.Request(env)

    request = normalize_request(raw_request)

    assert request.path == '/put'
    assert request.content_type == 'application/json'
    assert request.url == httpbin.url + '/put?key=val'
    assert request.method == 'put'
    assert request.body == '{"key2": "val2"}'

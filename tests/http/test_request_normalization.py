import pytest
import urllib

import six
from six.moves import urllib_parse as urlparse

import requests

from flex.http import (
    normalize_request, _tornado_available, _falcon_available, _webob_available,
    _django_available, _werkzeug_available, _aiohttp_available
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


@pytest.mark.skipif(not _webob_available, reason="webob not installed")
def test_webob_client_request_normalization(httpbin):
    import webob

    raw_request = webob.Request.blank(httpbin.url + '/get')
    raw_request.query_string = 'key=val'
    raw_request.method = 'GET'
    raw_request.content_type = 'application/json'

    request = normalize_request(raw_request)

    assert request.path == '/get'
    assert request.content_type == 'application/json'
    assert request.url == httpbin.url + '/get?key=val'
    assert request.method == 'get'


@pytest.mark.skipif(not _django_available, reason="django not installed")
def test_django_request_normalization(httpbin):
    from django.conf import settings
    if not settings.configured:
        settings.configure()
        settings.ALLOWED_HOSTS.append('127.0.0.1')

    import django.http.request

    url = urlparse.urlparse(httpbin.url + '/get')

    raw_request = django.http.request.HttpRequest()
    raw_request.method = 'GET'
    raw_request.path = url.path
    raw_request._body = None
    raw_request.META = {'CONTENT_TYPE': 'application/json', 'HTTP_HOST': url.netloc, 'QUERY_STRING': 'key=val'}

    request = normalize_request(raw_request)

    assert request.path == '/get'
    assert request.content_type == 'application/json'
    assert request.url == httpbin.url + '/get?key=val'
    assert request.method == 'get'

    del raw_request.META['CONTENT_TYPE']
    request = normalize_request(raw_request)
    assert request.content_type is None


@pytest.mark.skipif(not _werkzeug_available, reason="werkzeug not installed")
def test_werkzeug_request_normalization(httpbin):
    from werkzeug.test import create_environ
    from werkzeug.wrappers import Request

    env = create_environ(
        path='/put',
        base_url=httpbin.url,
        query_string='key=val',
        headers={'Content-Type': 'application/json'},
        data=b'{"key2": "val2"}',
        method='PUT',
    )
    raw_request = Request(env)
    request = normalize_request(raw_request)

    assert request.path == '/put'
    assert request.content_type == 'application/json'
    assert request.url == httpbin.url + '/put?key=val'
    assert request.method == 'put'
    assert request.data == {'key2': 'val2'}


@pytest.mark.skipif(not _aiohttp_available, reason="aiohttp not installed")
def test_aiohttp_request_normalization():
    from aiohttp.test_utils import make_mocked_request

    raw_request = make_mocked_request(
        'PUT', '/put', headers={'Content-Type': 'application/json'}, payload=b'{"key2": "val2"}'
    )
    request = normalize_request(raw_request)

    assert request.path == '/put'
    assert request.method == 'PUT'
    assert request.content_type == 'application/json'
    assert request.data == {'key2': 'val2'}
    assert request.headers.get('Content-Type') == 'application/json'

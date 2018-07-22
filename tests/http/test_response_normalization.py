from contextlib import closing
import pytest
import six
from six.moves import urllib_parse as urlparse

import urllib

import requests

from flex.http import (
    normalize_response, _tornado_available, _webob_available, _django_available,
    _werkzeug_available, _aiohttp_available
)


#
#  Test normalization of the response object from the requests library
#
def test_response_normalization(httpbin):
    raw_response = requests.get(httpbin.url + '/get')

    response = normalize_response(raw_response)

    assert response.path == '/get'
    assert response.content_type == 'application/json'
    assert response.url == httpbin.url + '/get'
    assert response.status_code == '200'


#
#  Test normalization of urllib response object
#
def test_urllib_response_normalization(httpbin):
    if six.PY2:
        raw_response = urllib.urlopen(httpbin.url + '/get')
    else:
        raw_response = urllib.request.urlopen(httpbin.url + '/get')

    response = normalize_response(raw_response)

    assert response.path == '/get'
    assert response.content_type == 'application/json'
    assert response.url == httpbin.url + '/get'
    assert response.status_code == '200'


#
#  Test normalization of urllib2 response object
#
@pytest.mark.skipif(six.PY3, reason="No urllib2 in python3")
def test_urllib2_response_normalization(httpbin):
    import urllib2
    raw_response = urllib2.urlopen(httpbin.url + '/get')

    response = normalize_response(raw_response)

    assert response.path == '/get'
    assert response.content_type == 'application/json'
    assert response.url == httpbin.url + '/get'
    assert response.status_code == '200'


#
# Test tornado response object
#
@pytest.mark.skipif(not _tornado_available, reason="tornado not installed")
def test_tornado_response_normalization(httpbin):
    import tornado.httpclient

    with closing(tornado.httpclient.HTTPClient()) as client:
        raw_response = client.fetch(
            httpbin.url + '/get',
            headers={'Content-Type': 'application/json'}
        )

    response = normalize_response(raw_response)

    assert response.path == '/get'
    assert response.content_type == 'application/json'
    assert response.url == httpbin.url + '/get'
    assert response.status_code == '200'


#
# Test webob response object
#
@pytest.mark.skipif(not _webob_available, reason="webob not installed")
def test_webob_response_normalization(httpbin):
    import webob

    raw_request = webob.Request.blank(httpbin.url + '/get')
    raw_request.query_string = 'key=val'
    raw_request.method = 'GET'
    raw_request.content_type = 'application/json'

    raw_response = webob.Response()
    raw_response.content_type = 'application/json'

    response = normalize_response(raw_response, raw_request)

    assert response.path == '/get'
    assert response.content_type == 'application/json'
    assert response.url == httpbin.url + '/get?key=val'
    assert response.status_code == '200'


@pytest.mark.skipif(not _django_available, reason="django not installed")
def test_django_response_normalization(httpbin):
    from django.conf import settings
    if not settings.configured:
        settings.configure()
        settings.ALLOWED_HOSTS.append('127.0.0.1')

    import django.http.request
    import django.http.response

    url = urlparse.urlparse(httpbin.url + '/get')

    raw_request = django.http.request.HttpRequest()
    raw_request.method = 'GET'
    raw_request.path = url.path
    raw_request._body = None
    raw_request.META = {'CONTENT_TYPE': 'application/json', 'HTTP_HOST': url.netloc, 'QUERY_STRING': 'key=val'}

    raw_response = django.http.response.HttpResponse(b'', content_type='application/json', status=200)

    response = normalize_response(raw_response, raw_request)

    assert response.path == '/get'
    assert response.content_type == 'application/json'
    assert response.url == httpbin.url + '/get?key=val'
    assert response.status_code == '200'

    del raw_response._headers['content-type']

    response = normalize_response(raw_response, raw_request)
    assert response.content_type is None

    redirect_url = 'http://www.example.org'
    raw_response = django.http.response.HttpResponseRedirect(redirect_url)

    response = normalize_response(raw_response)

    assert response.url == redirect_url


@pytest.mark.skipif(not _werkzeug_available, reason="django not installed")
def test_werkzeug_response_normalization(httpbin):
    from werkzeug.wrappers import Request, Response
    from werkzeug.test import create_environ

    raw_request = Request(create_environ(
        path='/get',
        base_url=httpbin.url,
        query_string='key=val',
        method='GET',
    ))

    raw_response = Response(
        response=b'{"key2": "val2"}',
        content_type='application/json',
    )

    response = normalize_response(raw_response, raw_request)

    assert response.path == '/get'
    assert response.content_type == 'application/json'
    assert response.url == httpbin.url + '/get?key=val'
    assert response.status_code == '200'


@pytest.mark.skipif(not _aiohttp_available, reason="aiohttp not installed")
def test_aiohttp_response_normalization():
    from aiohttp.test_utils import make_mocked_request
    from aiohttp.web import Response

    raw_request = make_mocked_request('GET', '/get?key=val')

    raw_response = Response(
        body=b'{"key2": "val2"}',
        content_type='application/json',
        headers={'Cache-Control': 'no-cache'}
    )

    response = normalize_response(raw_response, raw_request)

    assert response.path == '/get'
    assert response.data == {'key2': 'val2'}
    assert response.status_code == '200'
    assert response.headers.get('Cache-Control') == 'no-cache'

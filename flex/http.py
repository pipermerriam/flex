import six

import io
import http
import urllib

from six.moves import urllib_parse as urlparse
import json

from flex.constants import EMPTY

try:
    import tornado.httpclient
    import tornado.httpserver
except ImportError:
    _tornado_available = False
else:
    _tornado_available = True

try:
    import falcon  # noqa
except ImportError:
    _falcon_available = False
else:
    _falcon_available = True


class URLMixin(object):
    @property
    def url_components(self):
        return urlparse.urlparse(self.url)

    @property
    def path(self):
        return self.url_components.path

    @property
    def query(self):
        return self.url_components.query

    @property
    def query_data(self):
        return urlparse.parse_qs(self.query)


class Request(URLMixin):
    """
    Generic request object.  All supported requests are normalized to an
    instance of Request.
    """
    method = None

    def __init__(self, url, method, content_type=None, body=None, request=None, headers=None):
        self._request = request
        self.body = body
        self.url = url
        self.method = method
        self.content_type = content_type
        self.headers = headers or {}

    @property
    def data(self):
        """
        TODO: What is the right way to do this?
        """
        if not self.body:
            return self.body
        elif self.body is EMPTY:
            return EMPTY
        elif self.content_type.startswith('application/json'):
            return json.loads(self.body)
        elif self.content_type == 'application/x-www-form-urlencoded':
            return dict(urlparse.parse_qsl(self.body))
        else:
            raise NotImplementedError("No parser for content type")


def _normalize_requests_request(request):
    import requests

    if not isinstance(request, (requests.Request, requests.PreparedRequest)):
        raise TypeError("Cannot normalize this request object")

    url = request.url
    method = request.method.lower()
    content_type = request.headers.get('Content-Type')
    body = request.body

    return Request(
        url=url,
        body=body,
        method=method,
        content_type=content_type,
        request=request,
    )


def _normalize_python2_urllib_request(request):
    if six.PY2:
        import urllib2
        if not isinstance(request, urllib2.Request):
            raise TypeError("Cannot normalize this request object")
    else:
        raise TypeError("Cannot normalize python3 urllib request object")

    url = request.get_full_url()
    method = request.get_method().lower()
    content_type = request.headers.get('Content-type')
    body = request.get_data()

    return Request(
        url=url,
        body=body,
        method=method,
        content_type=content_type,
        request=request,
    )


def _normalize_python3_urllib_request(request):
    if six.PY3:
        if not isinstance(request, urllib.request.Request):
            raise TypeError("Cannot normalize this request object")
    else:
        raise TypeError("Cannot normalize python2 urllib request object")

    url = request.get_full_url()
    method = request.get_method().lower()
    content_type = request.headers.get('Content-type')
    body = request.data

    return Request(
        url=url,
        body=body,
        method=method,
        content_type=content_type,
        request=request,
    )


def _normalize_tornado_request(request):
    if not _tornado_available:
        raise TypeError("Tornado is not installed")

    if isinstance(request, tornado.httpclient.HTTPRequest):
        url = request.url
    elif isinstance(request, tornado.httpserver.HTTPRequest):
        # This is the only difference in their api that we care about.
        url = request.uri
    else:
        raise TypeError("Cannot normalize this request object")

    return Request(
        url=url,
        body=request.body,
        method=request.method.lower(),
        content_type=request.headers.get('Content-Type'),
        request=request,
    )


def _normalize_falcon_request(request):
    if not _falcon_available:
        raise TypeError("Falcon is not installed")

    # Falcon request.stream has to be replaced because it can be read only once
    request.stream = io.BytesIO(request.stream.read())

    return Request(
        url=request.url,
        body=request.stream.getvalue().decode(),
        method=request.method.lower(),
        content_type=request.content_type,
        request=request,
    )


REQUEST_NORMALIZERS = (
    _normalize_python2_urllib_request,
    _normalize_python3_urllib_request,
    _normalize_requests_request,
    _normalize_tornado_request,
    _normalize_falcon_request,
)


def normalize_request(request):
    """
    Given a request, normalize it to the internal Request class.
    """
    if isinstance(request, Request):
        return request

    for normalizer in REQUEST_NORMALIZERS:
        try:
            return normalizer(request)
        except TypeError:
            continue

    raise ValueError("Unable to normalize the provided request")


class Response(URLMixin):
    """
    Generic response object.  All supported responses are normalized to an
    instance of this Response.
    """
    _response = None
    status_code = None

    def __init__(self, request, content, url, status_code, content_type,
                 headers=None, response=None):
        self._response = response
        self.request = request
        self.content = content
        self.url = url
        self.status_code = str(status_code)
        self.content_type = content_type
        self.headers = headers or {}

    @property
    def path(self):
        return urlparse.urlparse(self.url).path

    @property
    def data(self):
        if self.content is EMPTY:
            return self.content
        elif self.content_type == 'application/json':
            if isinstance(self.content, six.binary_type):
                return json.loads(six.text_type(self.content, encoding='utf-8'))
            else:
                return json.loads(self.content)
        raise NotImplementedError("No content negotiation for this content type")


def _normalize_requests_response(response, request=None):
    import requests
    if not isinstance(response, requests.Response):
        raise TypeError("Cannot normalize this response object")

    url = response.url
    status_code = response.status_code
    content_type = response.headers.get('Content-Type')

    return Response(
        request=request,
        content=response.content,
        url=url,
        status_code=status_code,
        content_type=content_type,
        response=response,
    )


def _normalize_urllib_response(response, request=None):
    if six.PY2:
        if not isinstance(response, urllib.addinfourl):
            raise TypeError("Cannot normalize this response object")
    else:
        if not isinstance(response, http.client.HTTPResponse):
            raise TypeError("Cannot normalize this response object")

    url = response.url
    status_code = response.getcode()
    content_type = response.headers.get('Content-Type')

    return Response(
        request=request,
        content=response.read(),
        url=url,
        status_code=status_code,
        content_type=content_type,
        response=response,
    )


def _normalize_tornado_response(response, request=None):
    if not _tornado_available:
        raise TypeError("Tornado is not installed")

    if not isinstance(response, tornado.httpclient.HTTPResponse):
        raise TypeError("Cannot normalize this response object")

    return Response(
        request=request,
        content=response.body,
        url=response.effective_url,
        status_code=response.code,
        content_type=response.headers.get('Content-Type'),
        response=response,
    )


RESPONSE_NORMALIZERS = (
    _normalize_urllib_response,
    _normalize_requests_response,
    _normalize_tornado_response,
)


def normalize_response(response, request=None):
    """
    Given a response, normalize it to the internal Response class.  This also
    involves normalizing the associated request object.
    """
    if isinstance(response, Response):
        return response
    if request is not None and not isinstance(request, Request):
        request = normalize_request(request)

    for normalizer in RESPONSE_NORMALIZERS:
        try:
            return normalizer(response, request=request)
        except TypeError:
            continue

    raise ValueError("Unable to normalize the provided response")

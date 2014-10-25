import urlparse
import json


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

    def __init__(self, url, method, content_type=None, body=None, request=None):
        self._request = request
        self.body = body
        self.url = url
        self.method = method
        self.content_type = content_type


def normalize_request(request):
    """
    Given a request, normalize it to the internal Request class.
    """
    url = request.url
    method = request.method.lower()
    content_type = request.headers.get('Content-Type')

    return Request(
        url=url,
        method=method,
        content_type=content_type,
        request=request,
    )


class Response(URLMixin):
    """
    Generic response object.  All supported responses are normalized to an
    instance of this Response.
    """
    _response = None
    status_code = None

    def __init__(self, request, content, url, status_code, content_type, response=None):
        self._response = response
        self.request = request
        self.content = content
        self.url = url
        self.status_code = status_code
        self.content_type = content_type

    @property
    def path(self):
        return urlparse.urlparse(self.url).path

    @property
    def data(self):
        # TODO: content negotiation
        return json.loads(self.content)


def normalize_response(response):
    """
    Given a response, normalize it to the internal Response class.  This also
    involves normalizing the associated request object.
    """
    request = normalize_request(response.request)

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

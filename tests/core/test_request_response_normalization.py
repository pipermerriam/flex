import requests

from flex.http import (
    normalize_request,
    normalize_response,
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
#  Test normalizatin of the response object from the requests library
#
def test_response_normalization(httpbin):
    raw_response = requests.get(httpbin.url + '/get')

    response = normalize_response(raw_response)

    assert response.path == '/get'
    assert response.content_type == 'application/json'
    assert response.url == httpbin.url + '/get'
    assert response.status_code == 200

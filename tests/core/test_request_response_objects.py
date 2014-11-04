from flex.http import (
    Request,
    Response,
)

from tests.factories import (
    RequestFactory,
    ResponseFactory,
)


def test_path_property():
    request = RequestFactory(url='http://www.example.com/blog/25')
    assert request.path == '/blog/25'


def test_query_property():
    request = RequestFactory(url='http://www.example.com/api/?token=1234&secret=abcd')
    assert request.query == 'token=1234&secret=abcd'


def test_query_data_for_singular_values():
    request = RequestFactory(url='http://www.example.com/api/?token=1234&secret=abcd')
    assert request.query_data == {'token': ['1234'], 'secret': ['abcd']}


def test_query_data_for_multi_value_keys():
    request = RequestFactory(
        url='http://www.example.com/api/?token=1234&token=5678&secret=abcd',
    )
    assert request.query_data == {'token': ['1234', '5678'], 'secret': ['abcd']}

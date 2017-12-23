import os.path
import pytest

from flex.core import load

DIR = os.path.dirname(os.path.abspath(__file__))


@pytest.mark.parametrize(
    'path',
    (
        pytest.mark.xfail(os.path.join(DIR, 'example_schemas/uber.yaml')),
        pytest.mark.xfail(os.path.join(DIR, 'example_schemas/petstore.yaml')),
        pytest.mark.xfail(os.path.join(DIR, 'example_schemas/petstore-expanded.yaml')),
        os.path.join(DIR, 'example_schemas/api-with-examples.yaml'),
    )
)
def test_load_and_parse_schema(path):
    load(path)


def test_oas():
    load('https://raw.githubusercontent.com/OAI/OpenAPI-Specification/master/examples/v3.0/petstore.yaml')

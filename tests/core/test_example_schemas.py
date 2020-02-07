import os.path
import pytest

from flex.core import load

DIR = os.path.dirname(os.path.abspath(__file__))


@pytest.mark.parametrize(
    'path',
    (
        pytest.param(os.path.join(DIR, 'example_schemas/uber.yaml'), marks=pytest.mark.xfail),
        pytest.param(os.path.join(DIR, 'example_schemas/petstore.yaml'), marks=pytest.mark.xfail),
        pytest.param(os.path.join(DIR, 'example_schemas/petstore-expanded.yaml'), marks=pytest.mark.xfail),
        os.path.join(DIR, 'example_schemas/api-with-examples.yaml'),
    )
)
def test_load_and_parse_schema(path):
    load(path)


@pytest.mark.parametrize(
    'path',
    (
        'https://raw.githubusercontent.com/OAI/OpenAPI-Specification/master/examples/v3.0/petstore.yaml',
        'https://raw.githubusercontent.com/OAI/OpenAPI-Specification/master/examples/v3.0/api-with-examples.yaml',
        'https://raw.githubusercontent.com/OAI/OpenAPI-Specification/master/examples/v3.0/callback-example.yaml',
        'https://raw.githubusercontent.com/OAI/OpenAPI-Specification/master/examples/v3.0/link-example.yaml',
        'https://raw.githubusercontent.com/OAI/OpenAPI-Specification/master/examples/v3.0/petstore-expanded.yaml',
        'https://raw.githubusercontent.com/OAI/OpenAPI-Specification/master/examples/v3.0/uspto.yaml',
    )
)
def test_oas_v3(path):
    load(path)

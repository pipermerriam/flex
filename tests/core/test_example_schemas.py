import os.path
import pytest

from flex.core import load

DIR = os.path.dirname(os.path.abspath(__file__))


@pytest.mark.parametrize(
    'path',
    (
        os.path.join(DIR, 'example_schemas/petstore.json'),
        os.path.join(DIR, 'example_schemas/petstore-simple.json'),
        os.path.join(DIR, 'example_schemas/petstore-minimal.json'),
        os.path.join(DIR, 'example_schemas/petstore-expanded.json'),
        os.path.join(DIR, 'example_schemas/petstore-with-external-docs.json'),
    )
)
def test_load_and_parse_schema(path):
    load(path)

import pytest

from flex.core import load
from flex.serializers.core import ParameterSerializer
from flex.paths import (
    PARAMETER_REGEX,
    escape_regex_special_chars,
    match_path_to_api_path,
    path_to_regex,
    path_to_pattern,
)
from flex.constants import (
    INTEGER,
    NUMBER,
    STRING,
)


@pytest.mark.parametrize(
    'input_,expected',
    (
        ('/get/{id}', set(['{id}'])),
        ('/get/{main_id}/nested/{id}', set(['{main_id}', '{id}'])),
    )
)
def test_parameter_regex(input_, expected):
    """
    Ensure that the regex used to match parametrized path components correctly
    matches the expected parts in a path.
    """
    actual = PARAMETER_REGEX.findall(input_)

    assert expected == set(actual)


@pytest.mark.parametrize(
    'input_,expected',
    (
        ('/something.json', '/something\.json'),
    ),
)
def test_regex_character_escaping(input_, expected):
    """
    Test that the expected characters get escaped.
    """
    actual = escape_regex_special_chars(input_)
    assert actual == expected


def test_path_to_pattern_with_single_parameter():
    input_ = '/get/{id}'
    expected = '^/get/(?P<id>.+)$'

    serializer = ParameterSerializer(
        data=[{
            'required': True,
            'type': STRING,
            'name': 'id',
            'in': 'path',
        }],
        many=True
    )
    assert serializer.is_valid(), serializer.errors
    parameters = serializer.save()
    actual = path_to_pattern(input_, parameters=parameters)

    assert actual == expected


def test_path_to_pattern_with_multiple_parameters():
    input_ = '/get/{first_id}/then/{second_id}/'
    expected = '^/get/(?P<first_id>.+)/then/(?P<second_id>.+)/$'

    serializer = ParameterSerializer(
        data=[
            {'required': True, 'name': 'first_id', 'in': 'path', 'type': STRING},
            {'required': True, 'name': 'second_id', 'in': 'path',  'type': STRING},
        ],
        many=True
    )
    assert serializer.is_valid(), serializer.errors
    parameters = serializer.save()
    actual = path_to_pattern(input_, parameters=parameters)

    assert actual == expected


@pytest.mark.parametrize(
    'path',
    (
        '/basic_path',
        '/something.json',
        '/path-with-dashes',
        '/a/deeper/path/',
    ),
)
def test_path_to_regex_conversion_for_non_parametrized_paths(path):
    regex = path_to_regex(path, [])
    assert regex.match(path)


@pytest.mark.parametrize(
    'path,bad_path',
    (
        ('/something.json', '/something_json'),
        ('/something', '/something-with-extra'),
    ),
)
def test_path_to_regex_does_not_overmatch(path, bad_path):
    regex = path_to_regex(path, [])
    assert not regex.match(bad_path)


@pytest.mark.parametrize(
    'path,schema_path',
    (
        ('/api/path', '/path'),
        ('/api/path.json', '/path.json'),
        ('/api/get/1', '/get/{id}'),
    ),
)
def test_match_target_path_to_api_path(path, schema_path):
    schema = load('tests/core/path_test_schema.yaml')
    paths = schema['paths']
    base_path = schema['basePath']

    path = match_path_to_api_path(
        path_definitions=paths,
        target_path=path,
        base_path=base_path,
    )
    assert path == schema_path

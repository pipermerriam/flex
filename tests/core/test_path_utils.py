import six

from flex.serializers.core import ParameterSerializer
from flex.paths import (
    get_path_parameter_values,
    get_parameter_names_from_path,
    path_to_pattern,
)
from flex.constants import (
    INTEGER,
    STRING,
    PATH,
)


ID_IN_PATH = {
    'name': 'id', 'in': PATH, 'description': 'id', 'type': INTEGER, 'required': True,
}
USERNAME_IN_PATH = {
    'name': 'username', 'in': PATH, 'description': 'username', 'type': STRING, 'required': True
}


#
#  get_path_parameter_values tests
#
def test_getting_parameter_values_from_path():
    serializer = ParameterSerializer(many=True, data=[
        ID_IN_PATH,
        USERNAME_IN_PATH,
    ])
    assert serializer.is_valid(), serializer.errors
    parameters = serializer.object

    values = get_path_parameter_values(
        request_path='/get/fernando/posts/1234/',
        api_path='/get/{username}/posts/{id}/',
        path_parameters=parameters
    )
    assert len(values) == 2
    assert 'username' in values
    assert 'id' in values
    assert isinstance(values['username'], six.string_types)
    assert isinstance(values['id'], int)


#
# get_parameter_names_from_path tests
#
def test_non_parametrized_path_returns_empty():
    path = "/get/with/no-parameters"
    names = get_parameter_names_from_path(path)
    assert len(names) == 0


def test_getting_names_from_parametrized_path():
    path = "/get/{username}/also/{with_underscores}/and/{id}"
    names = get_parameter_names_from_path(path)
    assert len(names) == 3
    assert ("username", "with_underscores", "id") == names


#
# path_to_pattern tests
#
def test_undeclared_api_path_parameters_are_skipped():
    """
    Test that parameters that are declared in the path string but do not appear
    in the parameter definitions are ignored.
    """
    path = '/get/{username}/posts/{id}/'
    serializer = ParameterSerializer(many=True, data=[
        ID_IN_PATH,
    ])
    assert serializer.is_valid(), serializer.errors
    parameters = serializer.object
    pattern = path_to_pattern(path, parameters)
    assert pattern == '^/get/\{username\}/posts/(?P<id>.+)/$'

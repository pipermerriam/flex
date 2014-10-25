from flex.decorators import rewrite_reserved_words
from flex.utils import cast_value_to_type


@rewrite_reserved_words
def is_match(parameter, **kwargs):
    for key, value in kwargs.items():
        if key not in parameter:
            return False
        elif parameter[key] != value:
            return False
    return True


@rewrite_reserved_words
def filter_parameters(parameters, **kwargs):
    return [p for p in parameters if is_match(p, **kwargs)]


@rewrite_reserved_words
def find_parameter(parameters, **kwargs):
    """
    Given a list of parameters, find the one with the given name.
    """
    matching_parameters = filter_parameters(parameters, **kwargs)
    if len(matching_parameters) == 1:
        return matching_parameters[0]
    elif len(matching_parameters) > 1:
        raise ValueError("More than 1 parameter matched")
    raise ValueError("No parameters matched")


def type_cast_parameters(parameter_values, parameter_definitions):
    typed_parameters = {}
    for key in parameter_values.keys():
        try:
            parameter_definition = find_parameter(parameter_definitions, name=key)
        except KeyError:
            continue
        if 'type' not in parameter_definition:
            continue
        value = parameter_values[key]
        typed_parameters[key] = cast_value_to_type(value, parameter_definition['type'])
    return typed_parameters


def merge_parameter_lists(*parameter_definitions):
    """
    Merge multiple lists of parameters into a single list.  If there are any
    duplicate definitions, the last write wins.
    """
    merged_parameters = {}
    for parameter_list in parameter_definitions:
        for parameter in parameter_list:
            key = (parameter['name'], parameter['in'])
            merged_parameters[key] = parameter
    return merged_parameters.values()

import collections

from flex.decorators import rewrite_reserved_words


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


def dereference_parameter_list(parameters, parameter_definitions):
    return [
        (p if isinstance(p, collections.Mapping) else parameter_definitions[p])
        for p in parameters
    ]

import collections
import functools
import re

from flex.constants import (
    PATH,
)
from flex.parameters import (
    find_parameter,
    merge_parameter_lists,
    dereference_parameter_list,
)


REGEX_REPLACEMENTS = (
    ('\.', '\.'),
    ('\{', '\{'),
    ('\}', '\}'),
)


def escape_regex_special_chars(api_path):
    """
    Turns the non prametrized path components into strings subtable for using
    as a regex pattern.  This primarily involves escaping special characters so
    that the actual character is matched in the regex.
    """
    def substitute(string, replacements):
        pattern, repl = replacements
        return re.sub(pattern, repl, string)

    return functools.reduce(substitute, REGEX_REPLACEMENTS, api_path)


# matches the parametrized parts of a path.
# eg. /{id}/ matches the `{id}` part of it.
PARAMETER_REGEX = re.compile('(\{[^\}]+})')


def construct_parameter_pattern(parameter):
    """
    Given a parameter definition returns a regex pattern that will match that
    part of the path.
    """
    name = parameter['name']

    return "(?P<{name}>.+)".format(name=name)


def process_path_part(part, parameters):
    """
    Given a part of a path either:
        - If it is a parameter:
            parse it to a regex group
        - Otherwise:
            escape any special regex characters
    """
    if PARAMETER_REGEX.match(part):
        parameter_name = part.strip('{}')
        try:
            parameter = find_parameter(parameters, name=parameter_name, in_=PATH)
        except ValueError:
            pass
        else:
            return construct_parameter_pattern(parameter)
    return escape_regex_special_chars(part)


def get_parameter_names_from_path(api_path):
    return tuple(p.strip('{}') for p in PARAMETER_REGEX.findall(api_path))


def path_to_pattern(api_path, parameters):
    """
    Given an api path, possibly with parameter notation, return a pattern
    suitable for turing into a regular expression which will match request
    paths that conform to the parameter definitions and the api path.
    """
    parts = re.split(PARAMETER_REGEX, api_path)
    pattern = ''.join((process_path_part(part, parameters) for part in parts))

    if not pattern.startswith('^'):
        pattern = "^{0}".format(pattern)
    if not pattern.endswith('$'):
        pattern = "{0}$".format(pattern)

    return pattern


def path_to_regex(api_path, path_parameters, global_parameters=None):
    if global_parameters is None:
        global_parameters = {}
    pattern = path_to_pattern(
        api_path=api_path,
        parameters=merge_parameter_lists(
            global_parameters.values(),
            dereference_parameter_list(path_parameters, global_parameters),
        ),
    )
    return re.compile(pattern)


def match_path_to_api_path(path_definitions, target_path, base_path='', global_parameters=None):
    """
    Match a request or response path to one of the api paths.

    Anything other than exactly one match is an error condition.
    """
    if global_parameters is None:
        global_parameters = {}
    assert isinstance(global_parameters, collections.Mapping)
    if target_path.startswith(base_path):
        target_path = target_path[len(base_path):]

    # Convert all of the api paths into Path instances for easier regex matching.
    paths = {
        p: path_to_regex(
            api_path=p,
            path_parameters=(v or {}).get('parameters', []),
            global_parameters=global_parameters,
        )
        for p, v in path_definitions.items()
    }

    matches = [p for p, r in paths.items() if r.match(target_path)]

    if not matches:
        raise LookupError('No paths found for {0}'.format(target_path))
    elif len(matches) > 1:
        raise LookupError('Multipue paths found for {0}.  Found `{1}`'.format(
            target_path, matches,
        ))
    else:
        return matches[0]

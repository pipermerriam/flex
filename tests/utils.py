import collections
import re
import six


def check_if_error_message_equal(formatted_msg, unformatted_msg):
    """
    Helper assertion for testing that a formatted error message matches the
    expected unformatted version of that error.
    """
    # Replace all `{}` style substitutions with `.*` so that we can run a regex
    # on the overall message, ignoring any pieces that would have been
    # dynamically inserted.
    if not isinstance(formatted_msg, six.string_types):
        raise ValueError(
            "formatted_msg must be a string: got `{0}`".format(
                repr(formatted_msg)),
        )
    if not isinstance(unformatted_msg, six.string_types):
        raise ValueError(
            "unformatted_msg must be a string: got `{0}`".format(
                repr(unformatted_msg)),
        )
    # replace any string formatters
    pattern = re.sub('\{.*\}', '.*', unformatted_msg)
    # replace any parenthesis
    pattern = re.sub('\(', '\(', pattern)
    pattern = re.sub('\)', '\)', pattern)
    # replace ^ and $
    pattern = re.sub('\^', '\^', pattern)
    pattern = re.sub('\$', '\$', pattern)

    return bool(re.compile(pattern).search(formatted_msg))


def assert_error_message_equal(formatted_msg, unformatted_msg):
    if not check_if_error_message_equal(formatted_msg, unformatted_msg):
        raise AssertionError(
            "`{0}` not found in `{1}`".format(
                formatted_msg, unformatted_msg,
            )
        )


def _find_message_in_errors(message, errors, namespace=''):
    if isinstance(errors, six.string_types):
        if check_if_error_message_equal(errors, message):
            yield namespace
    elif isinstance(errors, collections.Mapping):
        for key, error in errors.items():
            for match in _find_message_in_errors(
                message,
                error,
                '.'.join((namespace, key)).strip('.'),
            ):
                yield match
    elif isinstance(errors, list):
        for index, error in enumerate(errors):
            for match in _find_message_in_errors(
                message,
                error,
                '.'.join((namespace, six.text_type(index))).strip('.'),
            ):
                yield match
    else:
        raise ValueError("Unsupported type")


def find_message_in_errors(*args, **kwargs):
    paths = tuple(_find_message_in_errors(*args, **kwargs))
    return paths


def _find_matching_paths(target_path, paths):
    pattern = re.sub('\.', '.+', target_path)
    pattern = re.sub(r'^(.+)\^', r'\1\^', pattern)
    pattern = re.sub(r'\$(.+)$', r'\$\1', pattern)
    for message_path in paths:
        if re.search(pattern, message_path):
            yield message_path


def find_matching_paths(*args, **kwargs):
    paths = tuple(_find_matching_paths(*args, **kwargs))
    return paths


def assert_message_in_errors(message, errors, target_path=None):
    paths = tuple(_find_message_in_errors(message, errors))
    if not paths:
        raise AssertionError("Message: `{0}` not found in errors: `{1}`".format(
            message, errors,
        ))

    if target_path is not None:
        if not tuple(_find_matching_paths(target_path, paths)):
            raise AssertionError("No paths matched `{0}`.  Tried `{1}`".format(
                target_path, paths,
            ))


def assert_message_not_in_errors(message, errors):
    paths = tuple(_find_message_in_errors(message, errors))
    if paths:
        raise AssertionError(
            "Message: `{0}` found under paths: `{1}`".format(message, paths),
        )


def _enumerate_error_paths(errors, namespace=''):
    if isinstance(errors, six.string_types):
        yield namespace
    elif isinstance(errors, collections.Mapping):
        for key, error in errors.items():
            for match in _enumerate_error_paths(
                error,
                '.'.join((namespace, key)).strip('.'),
            ):
                yield match
    elif isinstance(errors, list):
        for index, error in enumerate(errors):
            for match in _enumerate_error_paths(
                error,
                '.'.join((namespace, six.text_type(index))).strip('.'),
            ):
                yield match
    else:
        raise ValueError("Unsupported type")


def enumerate_error_paths(*args, **kwargs):
    return tuple(_enumerate_error_paths(*args, **kwargs))


def assert_path_in_errors(path, errors):
    paths = find_matching_paths(path, enumerate_error_paths(errors))
    assert find_matching_paths(path, paths)


def assert_path_not_in_errors(path, errors):
    matches = find_matching_paths(path, enumerate_error_paths(errors))
    if matches:
        raise AssertionError(
            "The path {0} was found in the paths: {1}".format(repr(path), repr(matches)),
        )


def generate_validator_from_schema(schema, **kwargs):
    # TODO: switch this to new non-serializer validation
    from flex.serializers.core import SchemaSerializer

    serializer = SchemaSerializer(data=schema, **kwargs)
    assert serializer.is_valid(), serializer.errors

    validator = serializer.save()
    return validator

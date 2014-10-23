import re
import six


def assert_error_message_equal(formatted_msg, unformatted_msg):
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

    if not re.compile(pattern).search(formatted_msg):
        raise AssertionError(
            "`{0}` not found in `{1}`".format(
                formatted_msg, unformatted_msg,
            )
        )


def generate_validator_from_schema(schema, **kwargs):
    from flex.serializers.core import SchemaSerializer

    serializer = SchemaSerializer(data=schema, **kwargs)
    assert serializer.is_valid(), serializer.errors

    validator = serializer.save()
    return validator

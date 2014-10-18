import collections
import functools

from rest_framework import serializers

from flex.utils import (
    prettify_errors,
    is_value_of_any_type,
    is_non_string_iterable,
)


def validate_type(value, types):
    if not is_value_of_any_type(value, types):
        raise serializers.ValidationError("Invalid Type: {0}".format(value))


def generate_type_validator(types):
    if not is_non_string_iterable(types):
        types = (types,)
    return functools.partial(validate_type, types=types)


def validate_schema(obj, validators):
    errors = {}

    for key, value in validators.items():
        errors_ = collections.defaultdict(list)
        for attribute, validator in value.items():
            try:
                validator(obj[key])
            except serializers.ValidationError as err:
                errors_[attribute].append(err.messages)
        if errors_:
            errors[key] = [errors_]

    if errors:
        raise ValueError(prettify_errors(errors))

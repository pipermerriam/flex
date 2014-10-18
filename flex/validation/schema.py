import collections
import functools

from rest_framework import serializers

from flex.constants import PRIMATIVE_TYPES
from flex.utils import prettify_errors


def isinstance_(obj, classinfo):
    if not isinstance(obj, classinfo):
        raise serializers.ValidationError('Must be of type {0}'.format(classinfo))


def generate_type_validator(type):
    return functools.partial(isinstance_, classinfo=PRIMATIVE_TYPES[type])


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

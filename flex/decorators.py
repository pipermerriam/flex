import functools

from rest_framework import serializers

from flex.utils import (
    is_non_string_iterable,
    is_value_of_type,
    get_type_for_value,
)
from flex.constants import EMPTY


def maybe_iterable(func):
    @functools.wraps(func)
    def inner(value):
        if is_non_string_iterable(value):
            return map(func, value)
        else:
            return func(value)
    return inner


def enforce_type(type_):
    def outer(func):
        @functools.wraps(func)
        def inner(value, *args, **kwargs):
            if value is EMPTY or is_value_of_type(value, type_):
                return func(value, *args, **kwargs)
            else:
                raise serializers.ValidationError(
                    "Value must be of type {0}.  {1} is of type {2}".format(
                        type_, value, get_type_for_value(value),
                    ),
                )
        return inner
    return outer

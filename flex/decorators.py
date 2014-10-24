import functools

from flex.utils import (
    is_non_string_iterable,
    is_value_of_any_type,
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


def skip_if_not_of_type(*types):
    def outer(func):
        @functools.wraps(func)
        def inner(value, *args, **kwargs):
            if value is EMPTY or is_value_of_any_type(value, types):
                return func(value, *args, **kwargs)
        return inner
    return outer

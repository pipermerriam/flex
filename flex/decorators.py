import functools

from flex.utils import is_non_string_iterable


def maybe_iterable(func):
    @functools.wraps(func)
    def inner(value):
        if is_non_string_iterable(value):
            return map(func, value)
        else:
            return func(value)
    return inner

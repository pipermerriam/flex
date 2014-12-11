import functools

from flex.exceptions import ValidationError
from flex.utils import (
    is_non_string_iterable,
    is_value_of_any_type,
)
from flex.constants import EMPTY

from django.core.exceptions import ValidationError as DjangoValidationError


def maybe_iterable(func):
    @functools.wraps(func)
    def inner(value):
        if is_non_string_iterable(value):
            return list(map(func, value))
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


RESERVED_WORDS = (
    'in',
    'format',
    'type',
)


def rewrite_reserved_words(func):
    """
    Given a function whos kwargs need to contain a reserved word such as 'in',
    allow calling that function with the keyword as 'in_', such that function
    kwargs are rewritten to use the reserved word.
    """
    @functools.wraps(func)
    def inner(*args, **kwargs):
        for word in RESERVED_WORDS:
            key = "{0}_".format(word)
            if key in kwargs:
                kwargs[word] = kwargs.pop(key)
        return func(*args, **kwargs)
    return inner


def suffix_reserved_words(func):
    """
    Given a function that is called with a reseved word, rewrite the keyword
    with an underscore suffix.
    """
    @functools.wraps(func)
    def inner(*args, **kwargs):
        for word in RESERVED_WORDS:
            if word in kwargs:
                key = "{0}_".format(word)
                kwargs[key] = kwargs.pop(word)
        return func(*args, **kwargs)
    return inner


def translate_validation_error(func):
    """
    Given a function that potentially raises
    `django.core.exceptions.ValidationError`, reraise the same error as a
    `flex.exceptions.ValidationError`.
    """
    @functools.wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except DjangoValidationError as err:
            if isinstance(err, ValidationError):
                raise
            raise ValidationError(err.messages)
    return inner

import functools

import iso8601

from django.core.exceptions import ValidationError

from flex.utils import is_value_of_any_type
from flex.constants import (
    STRING,
)


class FormatRegistry(object):
    def __init__(self):
        self.formats = {}

    def register(self, format_name, *types):
        if format_name in self.formats:
            raise ValueError(
                "The format `{0}` is already registered".format(format_name),
            )

        def outer(func):
            @functools.wraps(func)
            def inner(value, *args, **kwargs):
                """
                Format validation should only be executed if the value is of
                one of the appropriate types for the format.

                http://json-schema.org/latest/json-schema-validation.html#anchor105
                """
                if is_value_of_any_type(value, types):
                    return func(value, *args, **kwargs)

            self.formats[format_name] = inner
            return inner
        return outer

    def __getitem__(self, key):
        return self.formats[key]

    def __contains__(self, key):
        return key in self.formats


registry = FormatRegistry()
register = registry.register


@register('date-time', STRING)
def date_time_format_validator(value):
    try:
        iso8601.parse_date(value)
    except iso8601.ParseError as e:
        raise ValidationError(e.message)

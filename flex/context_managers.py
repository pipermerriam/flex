import collections

from django.core.exceptions import ValidationError

from flex.exceptions import SafeNestedValidationError
from flex.utils import (
    prettify_errors,
)


class ErrorCollection(object):
    def __init__(self, inner=False, message='Invalid'):
        self.inner = inner
        self.message = message
        self.errors = collections.defaultdict(list)

    def __enter__(self):
        return self.errors

    def __exit__(self, type_, value, traceback):
        if any((type_, value, traceback)):
            if issubclass(type_, ValidationError):
                self.errors = value.messages
            else:
                return False
        if self.errors:
            if self.inner:
                raise SafeNestedValidationError(dict(self.errors))
            else:
                raise ValueError(self.message + '\n' + prettify_errors(self.errors))

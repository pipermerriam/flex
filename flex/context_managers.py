from flex.exceptions import (
    ValidationError,
    ErrorDict,
)


class ErrorCollection(object):
    def __init__(self, message='Invalid'):
        self.message = message
        self.errors = ErrorDict()

    def __enter__(self):
        return self.errors

    def __exit__(self, type_, value, traceback):
        if any((type_, value, traceback)):
            if issubclass(type_, ValidationError):
                self.errors = value.detail
            else:
                return False
        if self.errors:
            raise ValidationError(dict(self.errors))

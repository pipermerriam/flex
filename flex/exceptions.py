from rest_framework.serializers import NestedValidationError


class SafeNestedValidationError(NestedValidationError):
    def __repr__(self):
        return 'ValidationError({0})'.format(self.messages)

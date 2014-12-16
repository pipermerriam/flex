from flex.utils import is_value_of_type
from flex.decorators import (
    translate_validation_error,
)


class TypedDefaultMixin(object):
    default_error_messages = {
        'default_is_incorrect_type': (
            "The value supplied for 'default' must match the specified type."
        ),
    }

    def validate_default_type(self, attrs, errors):
        if 'default' in attrs and 'type' in attrs:
            if not is_value_of_type(attrs['default'], attrs['type']):
                errors['default'].add_error(
                    self.error_messages['default_is_incorrect_type'],
                )


class TranslateValidationErrorMixin(object):
    @translate_validation_error
    def field_from_native(self, *args, **kwargs):
        return super(TranslateValidationErrorMixin, self).field_from_native(
            *args, **kwargs
        )

    @translate_validation_error
    def validate(self, *args, **kwargs):
        return super(TranslateValidationErrorMixin, self).validate(
            *args, **kwargs
        )

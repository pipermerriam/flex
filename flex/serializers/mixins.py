from flex.utils import is_value_of_type


class TypedDefaultMixin(object):
    default_error_messages = {
        'default_is_incorrect_type': (
            "The value supplied for 'default' must match the specified type."
        ),
    }

    def validate_default_type(self, attrs, errors):
        if 'default' in attrs and 'type' in attrs:
            if not is_value_of_type(attrs['default'], attrs['type']):
                errors['default'].append(
                    self.error_messages['default_is_incorrect_type'],
                )

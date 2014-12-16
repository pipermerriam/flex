from rest_framework import serializers

from flex.exceptions import ValidationError
from flex.error_messages import MESSAGES
from flex.utils import is_non_string_iterable


class MaybeListCharField(serializers.CharField):
    def to_internal_value(self, data):
        if is_non_string_iterable(data):
            return data
        return super(MaybeListCharField, self).to_internal_value(data)


class SecurityReferencValidator(object):
    context = None

    def __call__(self, value):
        if self.context is None:
            raise ValueError("Missing validation context")
        if value not in self.context.get('securityDefinitions', {}):
            raise ValidationError(
                MESSAGES['unknown_reference']['security'].format(value),
            )

    def set_context(self, parent):
        self.context = parent.context


class SecurityRequirementReferenceField(serializers.CharField):
    """
    Field that references a defined security scheme declared in the Security
    Definitions.
    """
    def __init__(self, *args, **kwargs):
        super(SecurityRequirementReferenceField, self).__init__(*args, **kwargs)
        self.validators.append(SecurityReferencValidator())


class DefaultField(serializers.Field):
    def to_internal_value(self, data):
        return data

from flex.constants import (
    OBJECT,
)
from flex.decorators import (
    skip_if_not_of_type,
    skip_if_empty,
)
from flex.functional import (
    apply_functions_to_key,
)
from flex.validation.common import (
    generate_wrapped_validators,
    generate_object_validator,
)
from flex.validation.schema import (
    construct_schema_validators,
)

from .multiple_of import multiple_of_validator
from .maximum import maximum_validator
from .minimum import minimum_validator

'''
    multipleOf = serializers.FloatField(
        allow_null=True, required=False, validators=[MinValueValidator(0)],
    )

    maximum = serializers.FloatField(allow_null=True, required=False)
    exclusiveMaximum = serializers.NullBooleanField(required=False)

    minimum = serializers.FloatField(allow_null=True, required=False)
    exclusiveMinimum = serializers.NullBooleanField(required=False)

    maxLength = serializers.IntegerField(
        allow_null=True, required=False, validators=[MinValueValidator(0)],
    )
    minLength = serializers.IntegerField(
        allow_null=True, required=False, validators=[MinValueValidator(0)],
    )

    pattern = serializers.CharField(allow_null=True, required=False, validators=[regex_validator])

    maxItems = serializers.IntegerField(allow_null=True, required=False)
    minItems = serializers.IntegerField(allow_null=True, required=False)
    uniqueItems = serializers.NullBooleanField(required=False)

    enum = DefaultField(required=False, validators=[is_array_validator])
'''
schema_schema = {
    'type': OBJECT,
}
schema_validators = construct_schema_validators(schema_schema, {})


def validate_maximum_is_gte_minimum(obj):
    # TODO: we should know that these two values are valid.  Otherwise, we have
    # to reproduce all of the validation here.
    from flex.exceptions import ValidationError
    from flex.error_messages import MESSAGES
    minimum = obj.get('minimum')
    maximum = obj.get('maximum')
    if minimum and maximum and not maximum >= minimum:
        raise ValidationError(MESSAGES['maximum']['must_be_greater_than_minimum'])


extra_validators = {
    'multipleOf': skip_if_empty(skip_if_not_of_type(OBJECT)(
        apply_functions_to_key('multipleOf', multiple_of_validator),
    )),
    'maximum': skip_if_empty(skip_if_not_of_type(OBJECT)(
        generate_wrapped_validators(
            apply_functions_to_key('maximum', maximum_validator),
            validate_maximum_is_gte_minimum,
        ),
    )),
    'minimum': skip_if_empty(skip_if_not_of_type(OBJECT)(
        apply_functions_to_key('minimum', minimum_validator),
    )),
}
schema_validators.update(extra_validators)

schema_validator = generate_object_validator(schema_validators)

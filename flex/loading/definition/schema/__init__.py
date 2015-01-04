from flex.constants import (
    OBJECT,
    EMPTY,
)
from flex.decorators import (
    skip_if_not_of_type,
    skip_if_empty,
)
from flex.functional import (
    apply_functions_to_key,
)
from flex.validation.common import (
    generate_object_validator,
)
from flex.validation.schema import (
    construct_schema_validators,
)

from .multiple_of import multiple_of_validator

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


extra_validators = {
    'multipleOf': skip_if_empty(skip_if_not_of_type(OBJECT)(
        apply_functions_to_key('multipleOf', multiple_of_validator),
    )),
}
schema_validators.update(extra_validators)

schema_validator = generate_object_validator(schema_validators)

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
    generate_object_validator,
)
from flex.validation.schema import (
    construct_schema_validators,
)
from flex.datastructures import (
    ValidationDict,
)

from .multiple_of import multiple_of_validator
from .maximum import (
    maximum_validator,
    exclusive_maximum_validator,
    validate_maximum_is_gte_minimum,
    validate_maximum_required_if_exclusive_maximum_set,
)
from .minimum import (
    minimum_validator,
    exclusive_minimum_validator,
    validate_minimum_required_if_exclusive_minimum_set,
)
from .min_length import (
    min_length_validator,
)
from .max_length import (
    max_length_validator,
    validate_max_length_greater_than_or_equal_to_min_length,
)

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

schema_validators.add_property_validator('multipleOf', multiple_of_validator)
schema_validators.add_property_validator('minimum', minimum_validator)
schema_validators.add_property_validator('maximum', maximum_validator)
schema_validators.add_property_validator('exclusiveMinimum', exclusive_minimum_validator)
schema_validators.add_property_validator('exclusiveMaximum', exclusive_maximum_validator)
schema_validators.add_property_validator('minLength', min_length_validator)
schema_validators.add_property_validator('maxLength', max_length_validator)

non_field_validators = ValidationDict()
non_field_validators.add_validator(
    'maximum', validate_maximum_is_gte_minimum,
)
non_field_validators.add_validator(
    'maximum', validate_maximum_required_if_exclusive_maximum_set,
)
non_field_validators.add_validator(
    'minimum', validate_minimum_required_if_exclusive_minimum_set,
)
non_field_validators.add_validator(
    'maxLength', validate_max_length_greater_than_or_equal_to_min_length,
)

schema_validator = generate_object_validator(
    field_validators=schema_validators,
    non_field_validators=[non_field_validators],
)

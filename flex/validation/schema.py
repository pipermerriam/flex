import operator
import decimal
import collections
import functools

from django.core.validators import (
    MinLengthValidator,
    MaxLengthValidator,
)

from rest_framework import serializers

from flex.utils import (
    prettify_errors,
    is_value_of_any_type,
    is_non_string_iterable,
)


def validate_schema(obj, validators):
    """
    Given a json-like object to validate, and a dictionary of validators, apply
    the validators to the object.
    """
    errors = {}

    for key, value in validators.items():
        errors_ = collections.defaultdict(list)
        for attribute, validator in value.items():
            try:
                validator(obj[key])
            except serializers.ValidationError as err:
                errors_[attribute].append(err.messages)
        if errors_:
            errors[key] = [errors_]

    if errors:
        raise ValueError(prettify_errors(errors))


def validate_type(value, types):
    if not is_value_of_any_type(value, types):
        raise serializers.ValidationError("Invalid Type: {0}".format(value))


def generate_type_validator(**kwargs):
    types = kwargs['type']
    if not is_non_string_iterable(types):
        types = (types,)
    return functools.partial(validate_type, types=types)


def validate_multiple_of(value, divisor):
    """
    Given a value and a divisor, validate that the value is divisible by the
    divisor.
    """
    if not decimal.Decimal(str(value)) % decimal.Decimal(str(divisor)) == 0:
        raise serializers.ValidationError(
            "{0} is not a multiple of {1}".format(value, divisor),
        )


def generate_multiple_of_validator(multipleOf, **kwargs):
    return functools.partial(validate_multiple_of, divisor=multipleOf)


def validate_minimum(value, minimum, is_exclusive):
    if is_exclusive:
        comparison_text = "greater than"
        compare_fn = operator.gt
    else:
        comparison_text = "greater than or equal to"
        compare_fn = operator.ge

    if not compare_fn(value, minimum):
        raise serializers.ValidationError(
            "{0} must be {1} than {2}".format(value, comparison_text, minimum),
        )


def generate_minimum_validator(minimum, exclusiveMinimum=False, **kwargs):
    return functools.partial(validate_minimum, minimum=minimum, is_exclusive=exclusiveMinimum)


def validate_maximum(value, maximum, is_exclusive):
    if is_exclusive:
        comparison_text = "less than"
        compare_fn = operator.lt
    else:
        comparison_text = "less than or equal to"
        compare_fn = operator.le

    if not compare_fn(value, maximum):
        raise serializers.ValidationError(
            "{0} must be {1} than {2}".format(value, comparison_text, maximum),
        )


def generate_maximum_validator(maximum, exclusiveMaximum=False, **kwargs):
    return functools.partial(validate_maximum, maximum=maximum, is_exclusive=exclusiveMaximum)


def generate_min_length_validator(minLength, **kwargs):
    return MinLengthValidator(minLength)


def generate_max_length_validator(maxLength, **kwargs):
    return MaxLengthValidator(maxLength)


validator_mapping = {
    'type': generate_type_validator,
    'multipleOf': generate_multiple_of_validator,
    'minimum': generate_minimum_validator,
    'maximum': generate_maximum_validator,
    'minLength': generate_min_length_validator,
    'maxLength': generate_max_length_validator,
}


def generate_validator_for_schema(schema):
    # TODO: raise an error if there are unknown schema keys.
    validator = {}
    for key in schema:
        if key not in validator_mapping:
            # TODO: silent failure?
            continue
        validator[key] = validator_mapping[key](**schema)
    return validator

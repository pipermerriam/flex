import re
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


def validate_min_items(value, minimum):
    if len(value) < minimum:
        raise serializers.ValidationError(
            "Array must have at least {0} items.  It had {1}".format(
                minimum, len(value),
            ),
        )


def generate_min_items_validator(minItems, **kwargs):
    return functools.partial(validate_min_items, minimum=minItems)


def validate_max_items(value, maximum):
    if len(value) > maximum:
        raise serializers.ValidationError(
            "Array must have no more than {0} items.  It had {1}".format(
                maximum, len(value),
            ),
        )


def generate_max_items_validator(maxItems, **kwargs):
    return functools.partial(validate_max_items, maximum=maxItems)


def validate_unique_items(value):
    counter = collections.Counter(value)
    dupes = [v for v, count in counter.items() if count > 1]
    if dupes:
        raise serializers.ValidationError(
            "Items must be unique.  The following items appeard more than once: {0}".format(
                repr(dupes),
            ),
        )


def noop(*args, **kwargs):
    """
    No-Op validator that does nothing.
    """
    pass


def generate_unique_items_generator(uniqueItems, **kwargs):
    if uniqueItems:
        return validate_unique_items
    else:
        return noop


def deep_equal(a, b):
    """
    Because of things in python like:
        >>> 1 == 1.0
        True
        >>> 1 == True
        True
    """
    return a == b and isinstance(a, type(b))


def validate_enum(value, options):
    if not any(deep_equal(value, option) for option in options):
        raise serializers.ValidationError(
            "Invalid value.  {0} is not one of the available options ({1})".format(
                value, options,
            )
        )


def generate_enum_validator(enum, **kwargs):
    return functools.partial(validate_enum, options=enum)


def validate_min_properties(value, minimum):
    if len(value.keys()) < minimum:
        raise serializers.ValidationError(
            "Object must have more than {0} properties.  It had {1}".format(
                minimum, len(value.keys()),
            ),
        )


def generate_min_properties_validator(minProperties, **kwargs):
    return functools.partial(validate_min_properties, minimum=minProperties)


def validate_max_properties(value, maximum):
    if len(value.keys()) > maximum:
        raise serializers.ValidationError(
            "Object must have less than {0} properties.  It had {1}".format(
                maximum, len(value.keys()),
            ),
        )


def generate_max_properties_validator(maxProperties, **kwargs):
    return functools.partial(validate_max_properties, maximum=maxProperties)


def validate_pattern(value, regex):
    if not regex.match(value):
        raise serializers.ValidationError(
            "{0} did not match the pattern `{1}`.".format(value, regex.pattern),
        )


def generate_pattern_validator(pattern, **kwargs):
    return functools.partial(validate_pattern, regex=re.compile(pattern))


validator_mapping = {
    'type': generate_type_validator,
    'multipleOf': generate_multiple_of_validator,
    'minimum': generate_minimum_validator,
    'maximum': generate_maximum_validator,
    'minLength': generate_min_length_validator,
    'maxLength': generate_max_length_validator,
    'minItems': generate_min_items_validator,
    'maxItems': generate_max_items_validator,
    'uniqueItems': generate_unique_items_generator,
    'enum': generate_enum_validator,
    'minProperties': generate_min_properties_validator,
    'maxProperties': generate_max_properties_validator,
    'pattern': generate_pattern_validator,
}


def construct_schema_validator(schema):
    # TODO: raise an error if there are unknown schema keys.
    validator = {}
    for key in schema:
        if key not in validator_mapping:
            # TODO: silent failure?
            continue
        validator[key] = validator_mapping[key](**schema)
    return validator

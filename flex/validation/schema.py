import re
import itertools
import operator
import decimal
import collections
import functools

import six

from django.core.exceptions import ValidationError
from django.core.validators import (
    MinLengthValidator,
    MaxLengthValidator,
)

from flex.exceptions import SafeNestedValidationError
from flex.constants import (
    NUMBER,
    STRING,
    ARRAY,
    OBJECT,
    EMPTY,
)
from flex.decorators import skip_if_not_of_type
from flex.utils import (
    prettify_errors,
    is_value_of_any_type,
    is_non_string_iterable,
)
from flex.formats import registry


def skip_if_empty(func):
    @functools.wraps(func)
    def inner(value, *args, **kwargs):
        if value is EMPTY:
            return
        else:
            return func(value, *args, **kwargs)
    return inner


@skip_if_empty
def validate_type(value, types):
    if not is_value_of_any_type(value, types):
        raise ValidationError("Invalid Type: {0}".format(value))


def generate_type_validator(**kwargs):
    types = kwargs['type']
    if not is_non_string_iterable(types):
        types = (types,)
    return functools.partial(validate_type, types=types)


@skip_if_empty
@skip_if_not_of_type(NUMBER)
def validate_multiple_of(value, divisor):
    """
    Given a value and a divisor, validate that the value is divisible by the
    divisor.
    """
    if not decimal.Decimal(str(value)) % decimal.Decimal(str(divisor)) == 0:
        raise ValidationError(
            "{0} is not a multiple of {1}".format(value, divisor),
        )


def generate_multiple_of_validator(multipleOf, **kwargs):
    return functools.partial(validate_multiple_of, divisor=multipleOf)


@skip_if_empty
@skip_if_not_of_type(NUMBER)
def validate_minimum(value, minimum, is_exclusive):
    if is_exclusive:
        comparison_text = "greater than"
        compare_fn = operator.gt
    else:
        comparison_text = "greater than or equal to"
        compare_fn = operator.ge

    if not compare_fn(value, minimum):
        raise ValidationError(
            "{0} must be {1} than {2}".format(value, comparison_text, minimum),
        )


def generate_minimum_validator(minimum, exclusiveMinimum=False, **kwargs):
    return functools.partial(validate_minimum, minimum=minimum, is_exclusive=exclusiveMinimum)


@skip_if_empty
@skip_if_not_of_type(NUMBER)
def validate_maximum(value, maximum, is_exclusive):
    if is_exclusive:
        comparison_text = "less than"
        compare_fn = operator.lt
    else:
        comparison_text = "less than or equal to"
        compare_fn = operator.le

    if not compare_fn(value, maximum):
        raise ValidationError(
            "{0} must be {1} than {2}".format(value, comparison_text, maximum),
        )


def generate_maximum_validator(maximum, exclusiveMaximum=False, **kwargs):
    return functools.partial(validate_maximum, maximum=maximum, is_exclusive=exclusiveMaximum)


def generate_min_length_validator(minLength, **kwargs):
    return skip_if_empty(skip_if_not_of_type(STRING)(MinLengthValidator(minLength).__call__))


def generate_max_length_validator(maxLength, **kwargs):
    return skip_if_empty(skip_if_not_of_type(STRING)(MaxLengthValidator(maxLength).__call__))


@skip_if_empty
@skip_if_not_of_type(ARRAY)
def validate_min_items(value, minimum):
    if len(value) < minimum:
        raise ValidationError(
            "Array must have at least {0} items.  It had {1}".format(
                minimum, len(value),
            ),
        )


def generate_min_items_validator(minItems, **kwargs):
    return functools.partial(validate_min_items, minimum=minItems)


@skip_if_empty
@skip_if_not_of_type(ARRAY)
def validate_max_items(value, maximum):
    if len(value) > maximum:
        raise ValidationError(
            "Array must have no more than {0} items.  It had {1}".format(
                maximum, len(value),
            ),
        )


def generate_max_items_validator(maxItems, **kwargs):
    return functools.partial(validate_max_items, maximum=maxItems)


@skip_if_empty
@skip_if_not_of_type(ARRAY)
def validate_unique_items(value):
    counter = collections.Counter(value)
    dupes = [v for v, count in counter.items() if count > 1]
    if dupes:
        raise ValidationError(
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


@skip_if_empty
def validate_enum(value, options):
    if not any(deep_equal(value, option) for option in options):
        raise ValidationError(
            "Invalid value.  {0} is not one of the available options ({1})".format(
                value, options,
            )
        )


def generate_enum_validator(enum, **kwargs):
    return functools.partial(validate_enum, options=enum)


@skip_if_empty
@skip_if_not_of_type(OBJECT)
def validate_min_properties(value, minimum):
    if len(value.keys()) < minimum:
        raise ValidationError(
            "Object must have more than {0} properties.  It had {1}".format(
                minimum, len(value.keys()),
            ),
        )


def generate_min_properties_validator(minProperties, **kwargs):
    return functools.partial(validate_min_properties, minimum=minProperties)


@skip_if_empty
@skip_if_not_of_type(OBJECT)
def validate_max_properties(value, maximum):
    if len(value.keys()) > maximum:
        raise ValidationError(
            "Object must have less than {0} properties.  It had {1}".format(
                maximum, len(value.keys()),
            ),
        )


def generate_max_properties_validator(maxProperties, **kwargs):
    return functools.partial(validate_max_properties, maximum=maxProperties)


@skip_if_empty
@skip_if_not_of_type(STRING)
def validate_pattern(value, regex):
    if not regex.match(value):
        raise ValidationError(
            "{0} did not match the pattern `{1}`.".format(value, regex.pattern),
        )


def generate_pattern_validator(pattern, **kwargs):
    return functools.partial(validate_pattern, regex=re.compile(pattern))


def generate_format_validator(format, **kwargs):
    if format in registry:
        return registry[format]
    else:
        raise ValueError('Unknown format {0}'.format(format))


def validate_required(value):
    if value is EMPTY:
        raise ValidationError("This field is required.")


def generate_required_validator(required, **kwargs):
    if required:
        return validate_required
    else:
        return noop


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
    'format': generate_format_validator,
    'required': generate_required_validator,
}


def validate_schema(obj, validators, inner=None):
    """
    Given a json-like object to validate, and a dictionary of validators, apply
    the validators to the object.
    """
    errors = collections.defaultdict(list)

    if '$ref' in validators:
        ref_ = validators.pop('$ref', {})
        for k, v in ref_.validators.items():
            validators.setdefault(k, v)

    for key, validator in validators.items():
        try:
            validator(obj)
        except ValidationError as err:
            errors[key].extend(list(err.messages))

    if errors:
        if inner:
            raise SafeNestedValidationError(dict(errors))
        else:
            raise ValueError('Invalid:\n' + prettify_errors(errors))


def validate_properties(obj, key, validators):
    if obj is EMPTY:
        return
    validate_schema(obj.get(key, EMPTY), validators, inner=True)


def generate_items_validators(items, context):
    if isinstance(items, collections.Mapping):
        items_validators = construct_schema_validators(
            items,
            context,
        )
    elif isinstance(items, six.string_types):
        items_validators = {
            '$ref': LazyReferenceValidator(items, context),
        }
    else:
        assert 'Should not be possible'
    return items_validators


def validate_items(objs, validators):
    errors = []
    for obj, validator in zip(objs, validators):
        try:
            validate_schema(obj, validator, inner=True)
        except ValidationError as e:
            errors.extend(list(e.messages))

    if errors:
        raise SafeNestedValidationError(errors)


class LazyReferenceValidator(object):
    """
    This class acts as a lazy validator for references in schemas to prevent an
    infinite recursion error when a schema references itself, or there is a
    reference loop between more than one schema.

    The validator is only constructed if validator is needed.
    """
    def __init__(self, reference, context):
        # TODO: something better than this assertion
        assert 'definitions' in context
        assert reference in context['definitions']
        self.reference = reference
        self.context = context

    def __call__(self, value):
        return validate_schema(value, self.validators, inner=True)

    @property
    def validators(self):
        return construct_schema_validators(
            self.context['definitions'][self.reference],
            self.context,
        )

    def items(self):
        return self.validators.items()


def construct_schema_validators(schema, context):
    """
    Given a schema object, construct a dictionary of validators needed to
    validate a response matching the given schema.
    """
    validators = {}
    if '$ref' in schema:
        validators['$ref'] = LazyReferenceValidator(
            schema['$ref'],
            context,
        )
    if 'properties' in schema:
        intersection = set(schema['properties'].keys()).intersection(schema.keys())
        assert not intersection

        for property, property_schema in schema['properties'].items():
            property_validators = construct_schema_validators(
                property_schema,
                context,
            )
            validators[property] = functools.partial(
                validate_properties,
                key=property,
                validators=property_validators,
            )
    if 'items' in schema:
        items = schema['items']
        if isinstance(items, collections.Mapping) or isinstance(items, six.string_types):
            # If items is a reference or a schema, we pass it through as an
            # ever repeating list of the same validation dictionary, thus
            # validating all of the objects against the same schema.
            items_validators = itertools.repeat(generate_items_validators(
                items,
                context,
            ))
        elif isinstance(items, collections.Sequence):
            # We generate a list of validator dictionaries and then chain it
            # with an empty schema that repeats forever.  This ensures that if
            # the array of objects to be validated is longer than the array of
            # validators, then the extra elements will always validate since
            # they will be validated against an empty schema.
            items_validators = itertools.chain(
                map(functools.partial(generate_items_validators, context=context), items),
                itertools.repeat({}),
            )
        else:
            assert "Should not be possible"
        validators['items'] = functools.partial(
            validate_items, validators=items_validators,
        )
    for key in schema:
        if key in validator_mapping:
            validators[key] = validator_mapping[key](**schema)
    return validators

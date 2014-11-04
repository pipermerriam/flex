import functools

from django.core.exceptions import ValidationError

from flex.utils import is_non_string_iterable
from flex.context_managers import ErrorCollection
from flex.validation.common import (
    generate_type_validator,
    generate_format_validator,
    generate_required_validator,
    generate_multiple_of_validator,
    generate_minimum_validator,
    generate_maximum_validator,
    generate_min_length_validator,
    generate_max_length_validator,
    generate_min_items_validator,
    generate_max_items_validator,
    generate_unique_items_validator,
    generate_pattern_validator,
    generate_enum_validator,
)
from flex.paths import get_path_parameter_values
from flex.constants import EMPTY


validator_mapping = {
    'type': generate_type_validator,
    'format': generate_format_validator,
    'required': generate_required_validator,
    'multipleOf': generate_multiple_of_validator,
    'minimum': generate_minimum_validator,
    'maximum': generate_maximum_validator,
    'minLength': generate_min_length_validator,
    'maxLength': generate_max_length_validator,
    'minItems': generate_min_items_validator,
    'maxItems': generate_max_items_validator,
    'uniqueItems': generate_unique_items_validator,
    'enum': generate_enum_validator,
    'pattern': generate_pattern_validator,
    # TODO
    # - items
    # - schema
}


def validate_path_parameters(request_path, api_path, path_parameters, inner=False):
    """
    Helper function for validating a request path
    """
    parameter_values = get_path_parameter_values(request_path, api_path, path_parameters)
    validate_parameters(parameter_values, path_parameters, inner=inner)


def validate_query_parameters(raw_query_data, query_parameters, inner=False):
    query_data = {}
    for key, value in raw_query_data.items():
        if is_non_string_iterable(value) and len(value) == 1:
            query_data[key] = value[0]
        else:
            query_data[key] = value
    validate_parameters(query_data, query_parameters, inner=inner)


def validate_parameters(parameter_values, parameters, inner=False):
    validators = construct_path_parameter_validators(parameters)

    with ErrorCollection(inner=inner) as errors:
        # we should have a validator for every parameter value
        assert not set(parameter_values.keys()).difference(validators.keys())

        for key, validator in validators.items():
            try:
                validator(parameter_values.get(key, EMPTY))
            except ValidationError as err:
                errors[key].extend(list(err.messages))


def construct_parameter_validators(parameter):
    """
    Constructs a dictionary of validator functions for the provided parameter
    definition.
    """
    validators = {}
    for key in parameter:
        if key in validator_mapping:
            validators[key] = validator_mapping[key](**parameter)
    return validators


def validate_parameter(value, validators, inner=False):
    """
    Takes the value for a parameter and applies a dictionary of validator
    functions, collecting and re-raising any validation erros that occur.
    """
    with ErrorCollection(inner=inner) as errors:
        for key, validator in validators.items():
            try:
                validator(value)
            except ValidationError as err:
                errors[key].extend(list(err.messages))


def construct_path_parameter_validators(parameters):
    """
    Given an iterable of parameters, returns a dictionary of validator
    functions for each parameter.  Note that this expects the parameters to be
    unique in their name value, and throws an error if this is not the case.
    """
    validators = {}
    for parameter in parameters:
        key = parameter['name']
        if key in validators:
            raise ValueError("Duplicate parameter name {0}".format(key))
        parameter_validators = construct_parameter_validators(parameter)
        validators[key] = functools.partial(
            validate_parameter,
            validators=parameter_validators,
            inner=True,
        )

    return validators

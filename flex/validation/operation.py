import functools
import operator

from django.core.exceptions import ValidationError

from flex.utils import chain_reduce_partial
from flex.context_managers import ErrorCollection
from flex.http import (
    Request,
    Response,
)
from flex.constants import (
    QUERY,
    PATH,
)
from flex.parameters import (
    filter_parameters,
    merge_parameter_lists,
)
from flex.validation.parameter import (
    validate_path_parameters,
    validate_query_parameters,
)


def validate_operation(request, validators, inner=False):
    with ErrorCollection(inner=inner) as errors:
        for key, validator in validators.items():
            try:
                validator(request)
            except ValidationError as err:
                errors[key].extend(list(err.messages))


def validate_request_content_type(request, content_types):
    assert isinstance(request, Request)
    if request.content_type not in content_types:
        raise ValidationError(
            'Invalid content type `{0}`.  Must be one of `{1}`.'.format(
                request.content_type, content_types,
            ),
        )


def generate_request_content_type_validator(consumes, **kwargs):
    validator = functools.partial(
        validate_request_content_type,
        content_types=consumes,
    )
    return chain_reduce_partial(
        operator.attrgetter('request'),
        validator,
    )


def validate_response_content_type(response, content_types):
    assert isinstance(response, Response)  # TODO: remove this sanity check
    if response.content_type not in content_types:
        raise ValidationError(
            'Invalid content type `{0}`.  Must be one of `{1}`.'.format(
                response.content_type, content_types,
            ),
        )


def generate_response_content_type_validator(produces, **kwargs):
    return functools.partial(
        validate_response_content_type,
        content_types=produces,
    )


def validate_request_parameters(request, validators):
    with ErrorCollection(inner=True) as errors:

        for key, fn in validators.items():
            try:
                fn(request)
            except ValidationError as err:
                errors[key].extend(list(err.messages))


def generate_path_parameters_validator(api_path, path_parameters):
    path_parameter_validator = functools.partial(
        validate_path_parameters,
        api_path=api_path,
        path_parameters=path_parameters,
        inner=True,
    )
    return chain_reduce_partial(
        operator.attrgetter('path'),
        path_parameter_validator,
    )


def generate_query_parameters_validator(query_parameters):
    query_parameter_validator = functools.partial(
        validate_query_parameters,
        query_parameters=query_parameters,
        inner=True,
    )
    return chain_reduce_partial(
        operator.attrgetter('query_data'),
        query_parameter_validator,
    )


def generate_parameters_validator(api_path, path_definition, parameters, **kwargs):
    """
    Generates a validator function to validate.

    - request.path against the path parameters.
    - request.query against the query parameters.
    - TODO: request.headers against the header parameters.
    - TODO: request.body against the body parameters.
    - TODO: request.formData against any form data.
    """
    validators = {}
    path_level_parameters = path_definition.get('parameters', [])
    operation_level_parameters = parameters

    all_parameters = merge_parameter_lists(
        path_level_parameters,
        operation_level_parameters,
    )

    # PATH
    in_path_parameters = filter_parameters(all_parameters, in_=PATH)
    validators['path'] = generate_path_parameters_validator(api_path, in_path_parameters)

    # QUERY
    in_query_parameters = filter_parameters(all_parameters, in_=QUERY)
    validators['query'] = generate_query_parameters_validator(in_query_parameters)

    return chain_reduce_partial(
        operator.attrgetter('request'),
        functools.partial(validate_request_parameters, validators=validators),
    )


validator_mapping = {
    'consumes': generate_request_content_type_validator,
    'produces': generate_response_content_type_validator,
    'parameters': generate_parameters_validator,
}


def construct_operation_validators(api_path, path_definition, operation, context):
    validators = {}

    # - consumes (did the request conform to the content types this api consumes)
    # - produces (did the response conform to the content types this endpoint produces)
    # - parameters (did the parameters of this request validate)
    #   TODO: move path parameter validation to here, because each operation
    #         can override any of the path level parameters.
    # - schemes (was the request scheme correct)
    # - security: TODO since security isn't yet implemented.
    try:
        operation_definition = path_definition[operation]
    except KeyError:
        raise ValidationError(
            'Unknown operation `{0}`.  Must be one of `{1}`'.format(
                operation, path_definition.keys(),
            ),
        )

    # sanity check
    assert 'context' not in operation_definition
    assert 'api_path' not in operation_definition
    assert 'path_definition' not in operation_definition

    for key, value in operation_definition.items():
        if key not in validator_mapping:
            # TODO: is this the right thing to do?
            continue
        validators[key] = validator_mapping[key](
            context=context,
            api_path=api_path,
            path_definition=path_definition,
            **operation_definition
        )

    # Global defaults
    if 'consumes' in context and 'consumes' not in validators:
        validators['consumes'] = validator_mapping['consumes'](**context)
    if 'produces' in context and 'produces' not in validators:
        validators['produces'] = validator_mapping['produces'](**context)
    if 'parameters' in path_definition and 'parameters' not in validators:
        validators['parameters'] = validator_mapping['parameters'](
            context=context,
            api_path=api_path,
            path_definition=path_definition,
            parameters=path_definition['parameters'],
            **operation_definition
        )

    return validators

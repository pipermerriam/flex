import functools

from django.core.exceptions import ValidationError

from flex.utils import chain_reduce_partial
from flex.context_managers import ErrorCollection
from flex.paths import (
    match_request_path_to_api_path,
)
from flex.validation.operation import (
    construct_operation_validators,
    validate_operation,
)
from flex.error_messages import MESSAGES
from flex.constants import REQUEST_METHODS
from flex.http import normalize_response


def validate_request_to_path(request, paths, base_path, context):
    """
    Given a request, check whether the path of the request matches any if the
    api paths.  Note that this does not do deep validation on the path
    parameters themselves, but only matches whether the request path *looks*
    like an api path.

    If so, return the api path and the path definitions.
    """
    try:
        api_path = match_request_path_to_api_path(
            path_definitions=paths,
            request_path=request.path,
            base_path=base_path,
        )
    except LookupError:
        raise ValidationError(MESSAGES['request']['unknown_path'])

    path_definition = paths[api_path] or {}
    return api_path, path_definition


def validate_request_method_to_operation(request, path_definition):
    """
    Given a request, validate that the request method is valid for the request
    path.

    If so, return the operation related to this request method.
    """
    method = request.method
    try:
        operation = path_definition[method]
    except KeyError:
        allowed_methods = set(REQUEST_METHODS).intersection(path_definition.keys())
        raise ValidationError(
            MESSAGES['request']['invalid_method'].format(
                method, allowed_methods,
            ),
        )
    return operation


def validate_status_code_to_response_definition(response, operation):
    """
    Given a response, validate that the response status code is in the accepted
    status codes defined by this endpoint.

    If so, return the response definition that corresponds to the status code.
    """
    status_code = response.status_code
    operation_responses = operation['responses']
    try:
        response_definition = operation_responses[status_code]
    except KeyError:
        raise ValidationError(
            MESSAGES['response']['invalid_status_code'].format(
                status_code, operation_responses.keys(),
            ),
        )
    return response_definition


def validate_response(response, paths, base_path, context, inner=False):
    """
    Response validation involves the following steps.

       1. validate that the path matches one of the defined paths in the schema.
       2. validate that the request method conforms to a supported methods for the given path.
       3. validate that the request parameters conform to the parameter
          definitions for the operation definition.
       4. validate that the response status_code is in the allowed responses for
          the request method.
       5. validate that the response content validates against any provided
          schemas for the responses.
       6. headers, content-types, etc..., ???
    """
    with ErrorCollection(inner=inner) as errors:
        # 1
        try:
            api_path, path_definition = validate_request_to_path(
                request=response.request,
                paths=paths,
                base_path=base_path,
                context=context,
            )
        except ValidationError as err:
            errors['request'].extend(list(err.messages))
            return  # this causes an exception to be raised since errors is no longer falsy.

        if not path_definition:
            # TODO: is it valid to not have a definition for a path?
            return

        # 2
        try:
            operation = validate_request_method_to_operation(
                request=response.request,
                path_definition=path_definition,
            )
        except ValidationError as err:
            errors['request'].append(err.message)
            return

        if operation is None:
            # TODO: is this compliant with swagger, can path operations have a null
            # definition?
            return

        # 3
        operation_validators = construct_operation_validators(
            api_path=api_path,
            path_definition=path_definition,
            operation=response.request.method,
            context=context,
        )
        try:
            validate_operation(response, operation_validators, inner=True)
        except ValidationError as err:
            errors['request'].append(err.messages)

        # 4
        try:
            response_definition = validate_status_code_to_response_definition(  # NOQA
                response=response,
                operation=operation,
            )
        except ValidationError as err:
            errors['response'].append(err.message)
            return

        # 5
        # TODO

        # 6
        # TODO


def generate_response_validator(schema):
    response_validator = functools.partial(
        validate_response,
        paths=schema['paths'],
        base_path=schema.get('basePath', ''),
        context=schema,
    )
    return chain_reduce_partial(
        normalize_response,
        response_validator,
    )

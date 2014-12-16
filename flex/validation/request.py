import functools

from flex.utils import chain_reduce_partial
from flex.exceptions import ValidationError
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
from flex.http import normalize_request


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


def validate_request(request, paths, base_path, context, inner=False):
    """
    Request validation does the following steps.

       1. validate that the path matches one of the defined paths in the schema.
       2. validate that the request method conforms to a supported methods for the given path.
       3. validate that the request parameters conform to the parameter
          definitions for the operation definition.
    """
    with ErrorCollection(inner=inner) as errors:
        # 1
        try:
            api_path, path_definition = validate_request_to_path(
                request=request,
                paths=paths,
                base_path=base_path,
                context=context,
            )
        except ValidationError as err:
            errors['path'].add_error(err.detail)
            return  # this causes an exception to be raised since errors is no longer falsy.

        if not path_definition:
            # TODO: is it valid to not have a definition for a path?
            return

        # 2
        try:
            operation_definition = validate_request_method_to_operation(
                request=request,
                path_definition=path_definition,
            )
        except ValidationError as err:
            errors['method'].add_error(err.detail)
            return

        if operation_definition is None:
            # TODO: is this compliant with swagger, can path operations have a null
            # definition?
            return

        # 3
        operation_validators = construct_operation_validators(
            api_path=api_path,
            path_definition=path_definition,
            operation_definition=operation_definition,
            context=context,
        )
        try:
            validate_operation(request, operation_validators, inner=True)
        except ValidationError as err:
            errors['method'].add_error(err.detail)

    return operation_definition


def generate_request_validator(schema, **kwargs):
    request_validator = functools.partial(
        validate_request,
        paths=schema['paths'],
        base_path=schema.get('basePath', ''),
        context=schema,
        **kwargs
    )
    return chain_reduce_partial(
        normalize_request,
        request_validator,
    )

from __future__ import unicode_literals

from six.moves import urllib_parse as urlparse
import os
import collections
import requests

import six
import json
import yaml

from flex.context_managers import ErrorCollection
from flex.exceptions import ValidationError
from flex.serializers.core import (
    SwaggerSerializer,
    SchemaSerializer,
)
from flex.serializers.definitions import SwaggerDefinitionsSerializer
from flex.utils import prettify_errors
from flex.http import (
    normalize_request,
    normalize_response,
)
from flex.validation.request import validate_request
from flex.validation.response import validate_response


def load_source(source):
    """
    Common entry point for loading some form of raw swagger schema.

    Supports:
        - python object (dictionary-like)
        - path to yaml file
        - path to json file
        - file object (json or yaml).
        - json string.
        - yaml string.
    """
    if isinstance(source, collections.Mapping):
        return source
    elif hasattr(source, 'read') and callable(source.read):
        raw_source = source.read()
    elif os.path.exists(os.path.expanduser(str(source))):
        with open(os.path.expanduser(str(source)), 'r') as source_file:
            raw_source = source_file.read()
    elif isinstance(source, six.string_types):
        parts = urlparse.urlparse(source)
        if parts.scheme and parts.netloc:
            response = requests.get(source)
            if isinstance(response.content, six.binary_type):
                raw_source = six.text_type(response.content, encoding='utf-8')
            else:
                raw_source = response.content
        else:
            raw_source = source

    try:
        try:
            return json.loads(raw_source)
        except ValueError:
            pass

        try:
            return yaml.load(raw_source)
        except (yaml.scanner.ScannerError, yaml.parser.ParserError):
            pass
    except NameError:
        pass

    raise ValueError(
        "Unable to parse `{0}`.  Tried yaml and json.".format(source),
    )


def parse(raw_schema):
    definitions_serializer = SwaggerDefinitionsSerializer(
        data=raw_schema,
    )
    if not definitions_serializer.is_valid():
        message = "Swagger definitions did not validate:\n\n"
        message += prettify_errors(definitions_serializer.errors)
        raise ValueError(message)

    swagger_definitions = definitions_serializer.save()

    swagger_serializer = SwaggerSerializer(
        swagger_definitions,
        data=raw_schema,
        context=swagger_definitions,
    )

    if not swagger_serializer.is_valid():
        message = "Swagger schema did not validate:\n\n"
        message += prettify_errors(swagger_serializer.errors)
        raise ValueError(message)

    return swagger_serializer.save()


def load(target):
    """
    Given one of the supported target formats, load a swagger schema into it's
    python representation.
    """
    raw_schema = load_source(target)
    return parse(raw_schema)


def validate(schema, target=None, **kwargs):
    """
    Given the python representation of a JSONschema as defined in the swagger
    spec, validate that the schema complies to spec.  If `target` is provided,
    that target will be validated against the provided schema.
    """
    schema_serializer = SchemaSerializer(data=schema, **kwargs)
    if not schema_serializer.is_valid():
        message = "JSON Schema did not validate:\n\n"
        message += prettify_errors(schema_serializer.errors)
        raise ValidationError(message)

    if target is not None:
        validator = schema_serializer.save()
        validator(target)


def validate_api_call(schema, raw_request, raw_response):
    request = normalize_request(raw_request)
    response = normalize_response(raw_response)

    with ErrorCollection() as errors:
        try:
            validate_request(
                request=request,
                schema=schema,
            )
        except ValidationError as err:
            errors['request'].add_error(err.messages or getattr(err, 'detail'))
            return

        try:
            validate_response(
                response=response,
                request_method=request.method,
                schema=schema,
            )
        except ValidationError as err:
            errors['response'].add_error(err.messages or getattr(err, 'detail'))

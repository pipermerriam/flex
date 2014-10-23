from __future__ import unicode_literals

import os
import collections

import six
import json
import yaml

from flex.serializers.core import (
    SwaggerSerializer,
    SchemaSerializer,
)
from flex.serializers.definitions import SwaggerDefinitionsSerializer
from flex.utils import prettify_errors


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
        raw_source = source

    try:
        try:
            return yaml.load(raw_source)
        except yaml.scanner.ScannerError:
            pass

        try:
            return json.loads(raw_source)
        except ValueError:
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

    swagger_definitions = definitions_serializer.object

    swagger_serializer = SwaggerSerializer(
        swagger_definitions,
        data=raw_schema,
        context=swagger_definitions,
    )

    if not swagger_serializer.is_valid():
        message = "Swagger schema did not validate:\n\n"
        message += prettify_errors(swagger_serializer.errors)
        raise ValueError(message)

    return swagger_serializer.object


def load(target):
    raw_schema = load_source(target)
    return parse(raw_schema)


def validate(schema, target=None):
    schema_serializer = SchemaSerializer(data=schema)
    if not schema_serializer.is_valid():
        message = "JSON Schema did not validate:\n\n"
        message += prettify_errors(schema_serializer.errors)
        raise ValueError(message)

    if target is not None:
        validator = schema_serializer.save()
        validator(target)

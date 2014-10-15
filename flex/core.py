from __future__ import unicode_literals

import yaml

from flex.serializers.core import SwaggerSerializer
from flex.serializers.definitions import SwaggerDefinitionsSerializer
from flex.utils import prettify_errors


def load_source(source):
    # TODO: content negotiation.
    with open(source) as stream:
        raw_schema = yaml.load(stream)

    return raw_schema


def parse(raw_schema):
    definitions_serializer = SwaggerDefinitionsSerializer(
        data=raw_schema,
    )
    if not definitions_serializer.is_valid():

        message = "Swagger definitions did not validate:\n\n"
        message += '\n'.join(prettify_errors(definitions_serializer.errors))
        raise ValueError(message)

    swagger_definitions = definitions_serializer.object

    swagger_serializer = SwaggerSerializer(
        swagger_definitions,
        data=raw_schema,
        context=swagger_definitions,
    )

    if not swagger_serializer.is_valid():
        message = "Swagger schema did not validate:\n\n"
        message += '\n'.join(prettify_errors(swagger_serializer.errors))
        raise ValueError(message)

    return swagger_serializer.object


def load(target):
    raw_schema = load_source(target)
    return parse(raw_schema)

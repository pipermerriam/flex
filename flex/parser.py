from __future__ import unicode_literals

import yaml

from flex.serializers.core import SwaggerSerializer
from flex.serializers.definitions import SwaggerDefinitionsSerializer


def generate(path='flex/schema.yaml'):
    with open(path) as stream:
        schema = yaml.load(stream)

    swagger_definitions_serializer = SwaggerDefinitionsSerializer(
        data=schema,
        context={'foo': 'bar'},
    )
    assert swagger_definitions_serializer.is_valid(), swagger_definitions_serializer.errors

    swagger_definitions = swagger_definitions_serializer.object

    swagger_serializer = SwaggerSerializer(
        data=schema,
        context=swagger_definitions,
    )

    assert swagger_serializer.is_valid(), swagger_serializer.errors

    return swagger_serializer

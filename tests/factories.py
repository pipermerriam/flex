import factory

from flex.serializers.definitions import SwaggerDefinitionsSerializer
from flex.serializers.core import SwaggerSerializer
from flex.http import (
    Request,
    Response,
)


class RequestFactory(factory.Factory):
    url = 'http://www.example.com/'
    method = 'get'
    content_type = 'application/json'
    body = ''
    request = None

    class Meta:
        model = Request


class ResponseFactory(factory.Factory):
    url = 'http://www.example.com/'
    content_type = 'application/json'
    content = ''
    status_code = 200

    request = factory.SubFactory(
        RequestFactory, url=factory.SelfAttribute('..url'),
    )

    class Meta:
        model = Response


def SchemaFactory(**kwargs):
    kwargs.setdefault('swagger', '2.0')
    kwargs.setdefault('info', {'title': 'Test API', 'version': '0.0.1'})
    kwargs.setdefault('paths', {})


    definitions_serializer = SwaggerDefinitionsSerializer(
        data=kwargs,
    )
    assert definitions_serializer.is_valid(), definitions_serializer.errors

    swagger_serializer = SwaggerSerializer(
        definitions_serializer.object,
        data=kwargs,
        context=definitions_serializer.object,
    )

    assert swagger_serializer.is_valid(), swagger_serializer.errors
    return swagger_serializer.object

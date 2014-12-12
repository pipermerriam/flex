import rest_framework

__all__ = [
    'SwaggerDefinitionsSerializer',
    'DefinitionsSerializer',
    'SecuritySchemeSerializer',
    'SchemaSerializer',
    'HeaderSerializer',
    'ParameterDefinitionsSerializer',
    'ItemsSerializer',
]

if rest_framework.__version__ >= '3.0.0':
    from .drf_3.definitions import (
        SwaggerDefinitionsSerializer,
        DefinitionsSerializer,
        SecuritySchemeSerializer,
        SchemaSerializer,
        HeaderSerializer,
        ParameterDefinitionsSerializer,
        ItemsSerializer,
    )
else:
    from .drf_2.definitions import (
        SwaggerDefinitionsSerializer,
        DefinitionsSerializer,
        SecuritySchemeSerializer,
        SchemaSerializer,
        HeaderSerializer,
        ParameterDefinitionsSerializer,
        ItemsSerializer,
    )

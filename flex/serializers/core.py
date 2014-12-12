import rest_framework

__all__ = [
    'SwaggerSerializer',
    'SchemaSerializer',
    'PathsSerializer',
    'ParameterSerializer',
    'HeaderSerializer',
]

if rest_framework.__version__ >= '3.0.0':
    from .drf_3.core import (
        SwaggerSerializer,
        SchemaSerializer,
        PathsSerializer,
        ParameterSerializer,
        HeaderSerializer,
    )
else:
    from .drf_2.core import (
        SwaggerSerializer,
        SchemaSerializer,
        PathsSerializer,
        ParameterSerializer,
        HeaderSerializer,
    )

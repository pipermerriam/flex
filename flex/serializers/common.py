import rest_framework

__all__ = [
    'HomogenousDictSerializer',
    'BaseResponseSerializer',
    'BaseParameterSerializer',
    'BaseSchemaSerializer',
    'BaseItemsSerializer',
    'BaseHeaderSerializer',
]

if rest_framework.__version__ >= '3.0.0':
    from .drf_3.common import (
        HomogenousDictSerializer,
        BaseResponseSerializer,
        BaseParameterSerializer,
        BaseSchemaSerializer,
        BaseItemsSerializer,
        BaseHeaderSerializer,
    )
else:
    from .drf_2.common import (
        BaseHeaderSerializer,
        BaseItemsSerializer,
        BaseParameterSerializer,
        BaseResponseSerializer,
        BaseSchemaSerializer,
        HomogenousDictSerializer,
    )

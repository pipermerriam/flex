import rest_framework

__all__ = [
    'TypedDefaultMixin',
    'TranslateValidationErrorMixin',
]

if rest_framework.__version__ >= '3.0.0':
    from .drf_3.mixins import (
        TypedDefaultMixin,
        TranslateValidationErrorMixin,
    )
else:
    from .drf_2.mixins import (
        TypedDefaultMixin,
        TranslateValidationErrorMixin,
    )

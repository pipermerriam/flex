import rest_framework

__all__ = [
    'SecurityRequirementReferenceField',
    'MaybeListCharField',
]

if rest_framework.__version__ >= '3.0.0':
    from .drf_3.fields import (
        SecurityRequirementReferenceField,
        MaybeListCharField,
    )
else:
    from .drf_2.fields import (
        SecurityRequirementReferenceField,
        MaybeListCharField,
    )

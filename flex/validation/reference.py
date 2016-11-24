import os

from six.moves import urllib_parse as urlparse
import jsonpointer

from flex.validation.common import (
    validate_object,
)


class LazyReferenceValidator(object):
    """
    This class acts as a lazy validator for references in schemas to prevent an
    infinite recursion error when a schema references itself, or there is a
    reference loop between more than one schema.

    The validator is only constructed if validator is needed.
    """
    validators_constructor = None

    def __init__(self, reference, context, **kwargs):
        if self.validators_constructor is None:
            raise NotImplementedError(
                "Subclasses of LazyReferenceValidator must specify a "
                "`validators_constructor` function"
            )

        self._kwargs = kwargs

        parsed_ref = urlparse.urlparse(reference)
        self.reference_path = parsed_ref.path
        self.reference_fragment = parsed_ref.fragment

        if self.reference_path:
            from flex.core import load_source
            if self.reference_path.startswith('/'):
                context = load_source(self.reference_path)
            elif 'base_path' in kwargs:
                context = load_source(os.path.join(kwargs['base_path'], self.reference_path))

        # TODO: something better than this which potentiall raises a
        # JsonPointerException
        jsonpointer.resolve_pointer(context, self.reference_fragment)
        self.reference = reference
        self.context = context

    def __call__(self, value, **kwargs):
        return validate_object(
            value,
            schema=self.schema,
            **kwargs
        )

    @property
    def schema(self):
        return jsonpointer.resolve_pointer(self.context, self.reference_fragment)

    @property
    def validators(self):
        return self.validators_constructor(
            self.schema,
            self.context,
            **self._kwargs
        )

    def items(self):
        return self.validators.items()

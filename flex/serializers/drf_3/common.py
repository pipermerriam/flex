import copy
import six

from django.core.validators import (
    MinValueValidator,
)

from rest_framework import serializers
from rest_framework.utils import representation

from flex.error_messages import MESSAGES
from flex.exceptions import (
    ValidationError,
    ErrorDict,
)
from flex.utils import (
    is_value_of_any_type,
)
from flex.serializers.validators import (
    type_validator,
    format_validator,
    parameter_in_validator,
    collection_format_validator,
    regex_validator,
    is_array_validator,
    header_type_validator,
)
from flex.constants import (
    BODY,
    PATH,
    CSV,
    QUERY,
    FORM_DATA,
    MULTI,
    ARRAY,
    INTEGER,
    NUMBER,
    STRING,
    OBJECT,
)

from .fields import (
    MaybeListCharField,
    DefaultField,
)
from .mixins import (
    TypedDefaultMixin,
)


def make_serializer_repr_safe(serializer):
    """
    Since some of the serializers have recursive fields on them
    (`SchemaSerializer`), we need to avoid infinite recursion while
    trying to repr them.
    """
    serializer_copy = copy.deepcopy(serializer)

    for field_name in serializer_copy.fields.keys():
        field = serializer_copy.fields[field_name]
        if hasattr(field, 'child'):
            field = field.child
        if getattr(field, '_is_unsafe_to_repr', False):
            serializer_copy.fields.pop(field_name)
    return serializer_copy


class ReprSafeListSerializer(serializers.ListSerializer):
    def __repr__(self):
        return representation.serializer_repr(
            make_serializer_repr_safe(self.child),
            indent=1,
        )


class ReprSafeSerializer(object):
    def __repr__(self):
        """
        Since some of the serializers have recursive fields on them
        (`SchemaSerializer`), we need to avoid infinite recursion while
        trying to repr them.
        """
        return representation.serializer_repr(
            make_serializer_repr_safe(self),
            indent=1,
        )


class MaybeListSerializer(ReprSafeListSerializer):
    """
    For serializer fields that are allowed to be a reference, an object, or an
    iterable of objects.
    """
    def to_internal_value(self, data):
        if isinstance(data, list):
            return super(MaybeListSerializer, self).to_internal_value(data)
        return self.child.run_validation(data)


class BaseResponseSerializer(serializers.Serializer):
    """
    https://github.com/wordnik/swagger-spec/blob/master/versions/2.0.md#responseObject
    """
    description = serializers.CharField()


class HomogenousDictSerializer(ReprSafeSerializer, serializers.Serializer):
    """
    Serializes and object for which all of it's values should be valid against
    a specified serializer class.
    """
    value_serializer_class = None
    value_serializer_kwargs = None
    allow_empty = False

    def __init__(self, *args, **kwargs):
        self.value_serializer_kwargs = kwargs.pop(
            'value_serializer_kwargs',
            self.value_serializer_kwargs or {},
        )
        if self.value_serializer_class is None:
            raise ValueError(
                "Property `value_serializer_class` not declared on {0}".format(
                    type(self),
                ),
            )

        # populate fields for all of the keys in the object to be validated.
        data = kwargs.get('data')
        super(HomogenousDictSerializer, self).__init__(*args, **kwargs)
        self.create_fields_from_data(data)

    def create_fields_from_data(self, data):
        if data:
            fields = [
                key for key, value in data.items() if (value is not None or self.allow_empty)
            ]
            for field_name in fields:
                field_name = str(field_name)
                field = self.value_serializer_class(**self.value_serializer_kwargs)
                self.fields.setdefault(
                    field_name,
                    field,
                )

    def get_value(self, data):
        self.create_fields_from_data(data.get(self.field_name))
        return super(HomogenousDictSerializer, self).get_value(data)


class CommonJSONSchemaSerializer(ReprSafeSerializer, serializers.Serializer):
    default_error_messages = {
        'invalid_type_for_minimum': '`minimum` can only be used for json number types',
        'invalid_type_for_maximum': '`maximum` can only be used for json number types',
        'invalid_type_for_multiple_of': '`multipleOf` can only be used for json number types',
        'invalid_type_for_min_length': '`minLength` can only be used for string types',
        'invalid_type_for_max_length': '`maxLength` can only be used for string types',
        'invalid_type_for_min_items': '`minItems` can only be used for array types',
        'invalid_type_for_max_items': '`maxItems` can only be used for array types',
        'invalid_type_for_unique_items': '`uniqueItems` can only be used for array types',
        'exclusive_minimum_requires_minimum': (
            '`exclusiveMinimum` requires `minimum` to be set'
        ),
        'exclusive_maximum_requires_maximum': (
            '`exclusiveMaximum` requires `maximum` to be set'
        ),
        'enum_must_be_of_array_type': 'enum value must be an array',
    }

    multipleOf = serializers.FloatField(
        allow_null=True, required=False, validators=[MinValueValidator(0)],
    )

    maximum = serializers.FloatField(allow_null=True, required=False)
    exclusiveMaximum = serializers.NullBooleanField(required=False)

    minimum = serializers.FloatField(allow_null=True, required=False)
    exclusiveMinimum = serializers.NullBooleanField(required=False)

    maxLength = serializers.IntegerField(
        allow_null=True, required=False, validators=[MinValueValidator(0)],
    )
    minLength = serializers.IntegerField(
        allow_null=True, required=False, validators=[MinValueValidator(0)],
    )

    pattern = serializers.CharField(allow_null=True, required=False, validators=[regex_validator])

    maxItems = serializers.IntegerField(allow_null=True, required=False)
    minItems = serializers.IntegerField(allow_null=True, required=False)
    uniqueItems = serializers.NullBooleanField(required=False)

    enum = DefaultField(required=False, validators=[is_array_validator])

    class Meta:
        list_serializer_class = ReprSafeListSerializer

    def check_type_for_attr(self, attrs, field_name, types, errors, error_key):
        """
        Shortcut for common pattern of having a keyword that depends on the
        type of the object.  If the types provided do not have any intersection
        with the required types, then an error is created.
        """
        if field_name in attrs and 'type' in attrs:
            declared_types = attrs['type']
            if isinstance(declared_types, six.string_types):
                declared_types = [declared_types]

            if isinstance(types, six.string_types):
                types = [types]

            if not set(types).intersection(declared_types):
                errors[field_name].add_error(
                    self.error_messages[error_key],
                )

    def validate(self, attrs):
        errors = ErrorDict()

        # Minimum
        self.check_type_for_attr(
            attrs,
            'minimum',
            (INTEGER, NUMBER),
            errors,
            'invalid_type_for_minimum',
        )

        if 'exclusiveMinimum' in attrs and 'minimum' not in attrs:
            errors['exclusiveMinimum'].add_error(
                self.error_messages['exclusive_minimum_requires_minimum'],
            )

        # Maximum
        self.check_type_for_attr(
            attrs,
            'maximum',
            (INTEGER, NUMBER),
            errors,
            'invalid_type_for_maximum',
        )

        if 'exclusiveMaximum' in attrs and 'maximum' not in attrs:
            errors['exclusiveMaximum'].add_error(
                self.error_messages['exclusive_maximum_requires_maximum'],
            )

        # multipleOf
        self.check_type_for_attr(
            attrs,
            'multipleOf',
            (INTEGER, NUMBER),
            errors,
            'invalid_type_for_multiple_of',
        )

        # minLength
        self.check_type_for_attr(
            attrs,
            'minLength',
            STRING,
            errors,
            'invalid_type_for_min_length',
        )

        # maxLength
        self.check_type_for_attr(
            attrs,
            'maxLength',
            STRING,
            errors,
            'invalid_type_for_max_length',
        )

        # minItems
        self.check_type_for_attr(
            attrs,
            'minItems',
            ARRAY,
            errors,
            'invalid_type_for_min_items',
        )

        # maxItems
        self.check_type_for_attr(
            attrs,
            'maxItems',
            ARRAY,
            errors,
            'invalid_type_for_max_items',
        )

        # uniqueItems
        self.check_type_for_attr(
            attrs,
            'uniqueItems',
            ARRAY,
            errors,
            'invalid_type_for_unique_items',
        )

        # enum null value special case.
        if 'enum' in attrs and attrs['enum'] is None:
            errors['enum'].add_error(
                self.error_messages['enum_must_be_of_array_type'],
            )

        if errors:
            raise ValidationError(errors)
        return super(CommonJSONSchemaSerializer, self).validate(attrs)


class BaseSchemaSerializer(CommonJSONSchemaSerializer):
    """
    https://github.com/wordnik/swagger-spec/blob/master/versions/2.0.md#schemaObject
    """
    _is_unsafe_to_repr = True

    default_error_messages = {
        'invalid_type_for_min_properties': 'minProperties can only be used for `object` types',
        'invalid_type_for_max_properties': 'maxProperties can only be used for `object` types',
    }

    format = serializers.CharField(validators=[format_validator], allow_null=True, required=False)
    title = serializers.CharField(allow_null=True, required=False)
    default = DefaultField(allow_null=True, required=False)

    minProperties = serializers.IntegerField(
        allow_null=True, required=False, validators=[MinValueValidator(0)]
    )
    maxProperties = serializers.IntegerField(
        allow_null=True, required=False, validators=[MinValueValidator(0)],
    )

    required = serializers.NullBooleanField(required=False)
    type = MaybeListCharField(allow_null=True, required=False, validators=[type_validator])

    readOnly = serializers.NullBooleanField(required=False)
    externalDocs = serializers.CharField(allow_null=True, required=False)
    # TODO: how do we do example
    # example =

    # Not Implemented
    # xml
    # discriminator

    def validate(self, attrs):
        errors = ErrorDict()

        # minProperties
        self.check_type_for_attr(
            attrs,
            'minProperties',
            OBJECT,
            errors,
            'invalid_type_for_min_properties',
        )

        # maxProperties
        self.check_type_for_attr(
            attrs,
            'maxProperties',
            OBJECT,
            errors,
            'invalid_type_for_max_properties',
        )

        if errors:
            raise ValidationError(errors)
        return super(BaseSchemaSerializer, self).validate(attrs)

BaseSchemaSerializer._declared_fields['$ref'] = serializers.CharField(
    allow_null=True, required=False,
)


class BaseItemsSerializer(BaseSchemaSerializer):
    def run_validation(self, data):
        if not is_value_of_any_type(data, (ARRAY, OBJECT, STRING)):
            raise ValidationError([[{'non_field_errors': MESSAGES['items']['invalid_type']}]])
        return super(BaseItemsSerializer, self).run_validation(data)

    class Meta:
        list_serializer_class = MaybeListSerializer


class BaseParameterSerializer(TypedDefaultMixin, CommonJSONSchemaSerializer):
    """
    https://github.com/wordnik/swagger-spec/blob/master/versions/2.0.md#parameterObject
    """
    default_error_messages = {
        'path_parameters_are_required': (
            "A Parameter who's `in` value is 'path' must be declared as required."
        ),
        'schema_required': (
            "A Parameter who's `in` value is 'body' must declare a schema."
        ),
        'type_required': (
            "A Parameter who's `in` value is not 'body' must declare a type."
        ),
        'collection_format_must_be_multi': (
            "The collectionFormat 'multi' is only valid for `in` values of "
            "\"query\" or \"formData\"."
        ),
        'items_required': (
            "For type \"array\", the items parameter is required."
        ),
    }

    name = serializers.CharField()
    description = serializers.CharField(allow_null=True, required=False)
    required = serializers.NullBooleanField(required=False)

    type = MaybeListCharField(allow_null=True, required=False, validators=[type_validator])
    format = serializers.CharField(validators=[format_validator], allow_null=True, required=False)
    collectionFormat = serializers.CharField(
        allow_null=True, required=False, validators=[collection_format_validator], default=CSV,
    )
    default = DefaultField(allow_null=True, required=False)

    def validate(self, attrs):
        errors = ErrorDict()

        if attrs['in'] == PATH and not attrs.get('required'):
            errors['required'].add_error(
                self.error_messages['path_parameters_are_required'],
            )
        if attrs['in'] == BODY and not attrs.get('schema'):
            errors['schema'].add_error(
                self.error_messages['schema_required'],
            )
        if attrs['in'] != BODY:
            if 'type' not in attrs:
                errors['type'].add_error(
                    self.error_messages['type_required'],
                )
            if attrs.get('collectionFormat') == MULTI:
                if attrs['in'] not in (QUERY, FORM_DATA):
                    errors['collectionFormat'].add_error(
                        self.error_messages['collection_format_must_be_multi'],
                    )
            self.validate_default_type(attrs, errors)

        if attrs.get('type') == ARRAY and not attrs.get('items'):
            errors['items'].add_error(
                self.error_messages['items_required'],
            )

        if errors:
            raise ValidationError(errors)

        return super(BaseParameterSerializer, self).validate(attrs)

    def create(self, validated_data):
        return validated_data


class BaseHeaderSerializer(TypedDefaultMixin, CommonJSONSchemaSerializer):
    """
    https://github.com/wordnik/swagger-spec/blob/master/versions/2.0.md#header-object-
    """
    default_error_messages = {
        'items_required': (
            "When type is \"array\" the \"items\" is required"
        ),
    }
    description = serializers.CharField(allow_null=True, required=False)
    type = serializers.CharField(validators=[header_type_validator])
    format = serializers.CharField(validators=[format_validator], allow_null=True, required=False)
    collectionFormat = serializers.CharField(
        allow_null=True, required=False, validators=[collection_format_validator], default=CSV,
    )
    default = DefaultField(allow_null=True, required=False)

    def validate(self, attrs):
        errors = ErrorDict()

        if attrs.get('type') == ARRAY and 'items' not in attrs:
            errors['items'].add_error(
                self.error_messages['items_required'],
            )
        self.validate_default_type(attrs, errors)

        if errors:
            raise ValidationError(errors)
        return super(BaseHeaderSerializer, self).validate(attrs)

    def create(self, validated_data):
        return validated_data


# Cannot declare this as a property on the class because `in` is a reserved word.
BaseParameterSerializer._declared_fields['in'] = serializers.CharField(
    validators=[parameter_in_validator],
)

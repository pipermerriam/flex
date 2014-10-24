import collections
import six

from django.core.validators import (
    MinValueValidator,
)

from rest_framework import serializers

from flex.utils import (
    is_value_of_any_type,
)
from flex.serializers.fields import MaybeListCharField
from flex.serializers.mixins import (
    TypedDefaultMixin,
)
from flex.serializers.validators import (
    type_validator,
    format_validator,
    parameter_in_validator,
    collection_format_validator,
    regex_validator,
    is_array_validator,
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


class BaseResponseSerializer(serializers.Serializer):
    """
    https://github.com/wordnik/swagger-spec/blob/master/versions/2.0.md#responseObject
    """
    pass


class HomogenousDictSerializer(serializers.Serializer):
    """
    Serializes and object for which all of it's values should be valid against
    a specified serializer class.
    """
    value_serializer_class = None
    value_serializer_kwargs = None

    def __init__(self, *args, **kwargs):
        self.value_serializer_kwargs = {}
        if self.value_serializer_class is None:
            raise ValueError(
                "Property `value_serializer_class` not declared on {0}".format(
                    type(self),
                ),
            )

        # populate fields for all of the keys in the object to be validated.
        data = kwargs.get('data')
        super(HomogenousDictSerializer, self).__init__(*args, **kwargs)
        if data:
            for key in data:
                self.fields.setdefault(
                    key,
                    self.value_serializer_class(**self.value_serializer_kwargs),
                )

    def field_from_native(self, data, files, field_name, into):
        # populate fields for all of the keys in the object to be validated.
        if data.get(field_name):
            for key in data[field_name]:
                self.fields.setdefault(
                    key,
                    self.value_serializer_class(**self.value_serializer_kwargs),
                )
        return super(HomogenousDictSerializer, self).field_from_native(
            data, files, field_name, into,
        )


class CommonJSONSchemaSerializer(serializers.Serializer):
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
        required=False, validators=[MinValueValidator(0)],
    )

    maximum = serializers.FloatField(required=False)
    exclusiveMaximum = serializers.BooleanField(required=False)

    minimum = serializers.FloatField(required=False)
    exclusiveMinimum = serializers.BooleanField(required=False)

    maxLength = serializers.IntegerField(
        required=False, validators=[MinValueValidator(0)],
    )
    minLength = serializers.IntegerField(
        required=False, validators=[MinValueValidator(0)],
    )

    pattern = serializers.CharField(required=False, validators=[regex_validator])

    maxItems = serializers.IntegerField(required=False)
    minItems = serializers.IntegerField(required=False)
    uniqueItems = serializers.BooleanField(required=False)

    enum = serializers.WritableField(required=False, validators=[is_array_validator])

    def validate(self, attrs):
        errors = collections.defaultdict(list)

        # Minimum
        if 'minimum' in attrs and 'type' in attrs:
            if attrs['type'] not in (INTEGER, NUMBER):
                errors['minimum'].append(
                    self.error_messages['invalid_type_for_minimum'],
                )

        if 'exclusiveMinimum' in attrs and 'minimum' not in attrs:
            errors['exclusiveMinimum'].append(
                self.error_messages['exclusive_minimum_requires_minimum'],
            )

        # Maximum
        if 'maximum' in attrs and 'type' in attrs:
            if attrs['type'] not in (INTEGER, NUMBER):
                errors['maximum'].append(
                    self.error_messages['invalid_type_for_maximum'],
                )

        if 'exclusiveMaximum' in attrs and 'maximum' not in attrs:
            errors['exclusiveMaximum'].append(
                self.error_messages['exclusive_maximum_requires_maximum'],
            )

        # multipleOf
        if 'multipleOf' in attrs and 'type' in attrs:
            if attrs['type'] not in (INTEGER, NUMBER):
                errors['multipleOf'].append(
                    self.error_messages['invalid_type_for_multiple_of'],
                )

        # minLength
        if 'minLength' in attrs and 'type' in attrs:
            if attrs['type'] != STRING:
                errors['minLength'].append(
                    self.error_messages['invalid_type_for_min_length'],
                )

        # maxLength
        if 'maxLength' in attrs and 'type' in attrs:
            if attrs['type'] != STRING:
                errors['maxLength'].append(
                    self.error_messages['invalid_type_for_max_length'],
                )

        # maxItems
        if 'maxItems' in attrs and 'type' in attrs:
            if attrs['type'] != ARRAY:
                errors['maxItems'].append(
                    self.error_messages['invalid_type_for_max_items'],
                )

        # minItems
        if 'minItems' in attrs and 'type' in attrs:
            if attrs['type'] != ARRAY:
                errors['minItems'].append(
                    self.error_messages['invalid_type_for_min_items'],
                )

        # uniqueItems
        if 'uniqueItems' in attrs and 'type' in attrs:
            if attrs['type'] != ARRAY:
                errors['uniqueItems'].append(
                    self.error_messages['invalid_type_for_unique_items'],
                )

        # enum null value special case.
        if 'enum' in attrs and attrs['enum'] is None:
            errors['enum'].append(
                self.error_messages['enum_must_be_of_array_type'],
            )

        if errors:
            raise serializers.ValidationError(errors)
        return super(CommonJSONSchemaSerializer, self).validate(attrs)


class BaseSchemaSerializer(CommonJSONSchemaSerializer):
    """
    https://github.com/wordnik/swagger-spec/blob/master/versions/2.0.md#schemaObject
    """
    default_error_messages = {
        'invalid_type_for_min_properties': 'minProperties can only be used for `object` types',
        'invalid_type_for_max_properties': 'maxProperties can only be used for `object` types',
    }

    format = serializers.CharField(validators=[format_validator], required=False)
    title = serializers.CharField(required=False)
    default = serializers.WritableField(required=False)

    minProperties = serializers.IntegerField(
        required=False, validators=[MinValueValidator(0)]
    )
    maxProperties = serializers.IntegerField(
        required=False, validators=[MinValueValidator(0)],
    )

    required = serializers.BooleanField(required=False)
    type = MaybeListCharField(required=False, validators=[type_validator])

    readOnly = serializers.BooleanField(required=False)
    externalDocs = serializers.CharField(required=False)
    # TODO: how do we do example
    # example =

    # Not Implemented
    # xml
    # discriminator

    def validate(self, attrs):
        errors = collections.defaultdict(list)

        # minProperties
        if 'minProperties' in attrs and attrs.get('type') != OBJECT:
            errors['minProperties'].append(
                self.error_messages['invalid_type_for_min_properties'],
            )

        # maxProperties
        if 'maxProperties' in attrs and attrs.get('type') != OBJECT:
            errors['maxProperties'].append(
                self.error_messages['invalid_type_for_max_properties'],
            )

        if errors:
            raise serializers.ValidationError(errors)
        return super(BaseSchemaSerializer, self).validate(attrs)

BaseSchemaSerializer.base_fields['$ref'] = serializers.CharField(required=False)


class BaseItemsSerializer(BaseSchemaSerializer):
    default_error_messages = {
        'invalid_type_for_items': '`items` must be a referenc, a schema, or an array of schemas.',
    }

    def __init__(self, *args, **kwargs):
        if 'data' in kwargs:
            data = kwargs['data']
            if isinstance(data, collections.Mapping):
                kwargs['many'] = False
            elif isinstance(data, six.string_types):
                kwargs['many'] = False

        super(BaseItemsSerializer, self).__init__(*args, **kwargs)

    def from_native(self, data, files=None):
        if not is_value_of_any_type(data, (ARRAY, OBJECT, STRING)):
            raise serializers.ValidationError(
                self.error_messages['invalid_type_for_items']
            )
        return super(BaseItemsSerializer, self).from_native(data, files)


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
    description = serializers.CharField(required=False)
    required = serializers.BooleanField(required=False)

    type = MaybeListCharField(required=False, validators=[type_validator])
    format = serializers.CharField(validators=[format_validator], required=False)
    collectionFormat = serializers.CharField(
        required=False, validators=[collection_format_validator], default=CSV,
    )
    default = serializers.WritableField(required=False)

    @property
    def many(self):
        return True

    @many.setter
    def many(self, value):
        pass

    def validate(self, attrs):
        errors = collections.defaultdict(list)

        if attrs['in'] == PATH and not attrs.get('required'):
            errors['required'].append(
                self.error_messages['path_parameters_are_required'],
            )
        if attrs['in'] == BODY and not attrs.get('schema'):
            errors['schema'].append(
                self.error_messages['schema_required'],
            )
        if attrs['in'] != BODY:
            if 'type' not in attrs:
                errors['type'].append(
                    self.error_messages['type_required'],
                )
            if attrs.get('collectionFormat') == MULTI:
                if attrs['in'] not in (QUERY, FORM_DATA):
                    errors['collectionFormat'].append(
                        self.error_messages['collection_format_must_be_multi'],
                    )
            self.validate_default_type(attrs, errors)

        if attrs.get('type') == ARRAY and not attrs.get('items'):
            errors['items'].append(
                self.error_messages['items_required'],
            )

        if errors:
            raise serializers.ValidationError(errors)

        return super(BaseParameterSerializer, self).validate(attrs)


# Cannot declare this as a property on the class because `in` is a reserved word.
BaseParameterSerializer.base_fields['in'] = serializers.CharField(
    source='in', validators=[parameter_in_validator],
)

from __future__ import unicode_literals

import functools
import six

from rest_framework.fields import empty
from rest_framework import serializers

from flex.exceptions import (
    ValidationError,
    ErrorDict,
)
from flex.context_managers import ErrorCollection
from flex.serializers.datastructures import IntKeyedDict
from flex.serializers.validators import (
    host_validator,
    path_validator,
    scheme_validator,
    mimetype_validator,
    string_type_validator,
)
from flex.constants import (
    PATH,
    REQUEST_METHODS,
)
from flex.validation.common import (
    validate_object,
)
from flex.validation.schema import (
    construct_schema_validators,
)
from flex.paths import (
    get_parameter_names_from_path,
)
from flex.parameters import (
    filter_parameters,
    merge_parameter_lists,
    dereference_parameter_list,
)
from flex.error_messages import MESSAGES

from .fields import (
    SecurityRequirementReferenceField,
)
from .common import (
    HomogenousDictSerializer,
    BaseResponseSerializer,
    BaseParameterSerializer,
    BaseSchemaSerializer,
    BaseItemsSerializer,
    BaseHeaderSerializer,
)


class InfoSerializer(serializers.Serializer):
    """
    https://github.com/wordnik/swagger-spec/blob/master/versions/2.0.md#infoObject
    """
    title = serializers.CharField()
    description = serializers.CharField(allow_null=True, required=False)
    termsOfService = serializers.CharField(allow_null=True, required=False)
    contact = serializers.CharField(allow_null=True, required=False)
    license = serializers.CharField(allow_null=True, required=False)
    version = serializers.CharField(allow_null=True, required=False)


class ItemsSerializer(BaseItemsSerializer):
    def run_validation(self, data):
        if isinstance(data, six.string_types):
            value = self.to_internal_value(data)
            return value
        return super(ItemsSerializer, self).run_validation(data)

    def to_internal_value(self, data):
        if isinstance(data, six.string_types):
            definitions = self.context.get('definitions', {})
            if data not in definitions:
                raise ValidationError(
                    MESSAGES['unknown_reference']['definition'].format(data),
                )
            return data
        return super(ItemsSerializer, self).to_internal_value(data)


class HeaderSerializer(BaseHeaderSerializer):
    items = ItemsSerializer(allow_null=True, required=False, many=True)


class HeadersSerializer(HomogenousDictSerializer):
    """
    https://github.com/wordnik/swagger-spec/blob/master/versions/2.0.md#headersObject
    """
    value_serializer_class = HeaderSerializer


class SchemaSerializer(BaseSchemaSerializer):
    default_error_messages = {
        'unknown_reference': 'Unknown definition reference `{0}`'
    }

    def validate(self, attrs):
        errors = ErrorDict()

        if '$ref' in attrs:
            definitions = self.context.get('definitions', {})
            if attrs['$ref'] not in definitions:
                errors['$ref'].add_error(
                    self.error_messages['unknown_reference'].format(attrs['$ref']),
                )

        if errors:
            raise ValidationError(errors)
        return super(SchemaSerializer, self).validate(attrs)

    def create(self, validated_data):
        validators = construct_schema_validators(validated_data, self.context)
        return functools.partial(validate_object, validators=validators)


class ResponseSerializer(BaseResponseSerializer):
    """
    https://github.com/wordnik/swagger-spec/blob/master/versions/2.0.md#responseObject
    """
    schema = SchemaSerializer(allow_null=True, required=False)
    headers = HeadersSerializer(allow_null=True, required=False)
    # TODO: how do we do examples
    # examples =

    def get_value(self, data):
        return data.get(int(self.field_name), empty)


class ResponsesSerializer(HomogenousDictSerializer):
    value_serializer_class = ResponseSerializer
    value_serializer_kwargs = {'allow_null': True, 'required': False}

    def to_internal_value(self, data):
        value = super(ResponsesSerializer, self).to_internal_value(data)
        return IntKeyedDict(value)


class SecuritySerializer(HomogenousDictSerializer):
    value_serializer_class = SecurityRequirementReferenceField


class ParameterSerializer(BaseParameterSerializer):
    schema = SchemaSerializer(allow_null=True, required=False)
    items = ItemsSerializer(allow_null=True, required=False, many=True)

    def run_validation(self, data):
        if isinstance(data, six.string_types):
            value = self.to_internal_value(data)
            return value
        return super(ParameterSerializer, self).run_validation(data)

    def to_internal_value(self, data):
        if isinstance(data, six.string_types):
            self.validate_reference(data)
            return data
        return super(ParameterSerializer, self).to_internal_value(data)

    def validate_reference(self, reference):
        if reference not in self.context.get('parameters', {}):
            raise ValidationError(
                MESSAGES['unknown_reference']['parameter'].format(reference),
            )


class OperationSerializer(serializers.Serializer):
    """
    https://github.com/wordnik/swagger-spec/blob/master/versions/2.0.md#operationObject
    """
    tags = serializers.ListField(
        allow_null=True, required=False,
        child=serializers.CharField(
            allow_null=True, required=False, validators=[string_type_validator],
        ),
    )
    summary = serializers.CharField(allow_null=True, required=False)
    description = serializers.CharField(allow_null=True, required=False)
    externalDocs = serializers.CharField(allow_null=True, required=False)
    operationId = serializers.CharField(allow_null=True, required=False)
    consumes = serializers.ListField(
        allow_null=True, required=False,
        child=serializers.CharField(
            allow_null=True, required=False, validators=[mimetype_validator],
        ),
    )
    produces = serializers.ListField(
        allow_null=True, required=False,
        child=serializers.CharField(
            allow_null=True, required=False, validators=[mimetype_validator],
        ),
    )
    parameters = ParameterSerializer(allow_null=True, required=False, many=True)
    responses = ResponsesSerializer()
    schemes = serializers.ListField(
        allow_null=True, required=False,
        child=serializers.CharField(
            allow_null=True, required=False, validators=[scheme_validator],
        ),
    )
    deprecated = serializers.NullBooleanField(required=False)
    security = SecuritySerializer(allow_null=True, required=False)


class PathItemSerializer(serializers.Serializer):
    """
    https://github.com/wordnik/swagger-spec/blob/master/versions/2.0.md#pathsObject
    """
    # TODO. reference path item objects from definitions.
    # TODO. how is this supposted to work.  The swagger spec doesn't account
    # for a definitions location for PathItem definitions?
    # _ref = serializers.CharField(source='$ref')
    get = OperationSerializer(allow_null=True, required=False)
    put = OperationSerializer(allow_null=True, required=False)
    post = OperationSerializer(allow_null=True, required=False)
    delete = OperationSerializer(allow_null=True, required=False)
    options = OperationSerializer(allow_null=True, required=False)
    head = OperationSerializer(allow_null=True, required=False)
    patch = OperationSerializer(allow_null=True, required=False)
    # TODO: these can be a parameters reference object.
    parameters = ParameterSerializer(allow_null=True, required=False, many=True)

    """
    DRF3 splits `source` to populate source attrs which causes problems with
    any dotted paths, as `source.split('.')` is called.
    """
    @property
    def source_attrs(self):
        return [self.source]

    @source_attrs.setter
    def source_attrs(self, value):
        pass


class TagSerializer(serializers.Serializer):
    """
    https://github.com/wordnik/swagger-spec/blob/master/versions/2.0.md#tagObject
    """
    name = serializers.CharField()
    description = serializers.CharField(allow_null=True, required=False)
    externalDocs = serializers.CharField(allow_null=True, required=False)


class PropertiesSerializer(HomogenousDictSerializer):
    value_serializer_class = SchemaSerializer


# These fields include recursive use of the `SchemaSerializer` so they have to
# be attached after the `SchemaSerializer` class has been created.
SchemaSerializer._declared_fields['properties'] = PropertiesSerializer(
    allow_null=True, required=False,
)
SchemaSerializer._declared_fields['items'] = ItemsSerializer(
    allow_null=True, required=False, many=True,
)
SchemaSerializer._declared_fields['allOf'] = SchemaSerializer(
    allow_null=True, required=False, many=True,
)


class PathsSerializer(HomogenousDictSerializer):
    value_serializer_class = PathItemSerializer
    value_serializer_kwargs = {'allow_null': True}
    allow_empty = True

    def validate(self, attrs):
        with ErrorCollection() as errors:
            for api_path, path_definition in attrs.items():
                path_parameter_names = set(get_parameter_names_from_path(api_path))

                if path_definition is None:
                    continue

                api_path_level_parameters = dereference_parameter_list(
                    path_definition.get('parameters', []),
                    parameter_definitions=self.context.get('parameters', {}),
                )

                path_request_methods = set(REQUEST_METHODS).intersection(
                    path_definition.keys(),
                )

                if not path_request_methods:
                    for parameter in api_path_level_parameters:
                        if parameter['name'] not in path_parameter_names:
                            errors[api_path].add_error(
                                MESSAGES["path"]["missing_parameter"].format(
                                    parameter['name'], api_path,
                                ),
                            )

                for method, operation_definition in path_definition.items():
                    if method not in REQUEST_METHODS:
                        continue
                    if operation_definition is None:
                        operation_definition = {}
                    operation_level_parameters = dereference_parameter_list(
                        operation_definition.get('parameters', []),
                        parameter_definitions=self.context.get('parameters', {}),
                    )
                    parameters_in_path = filter_parameters(
                        merge_parameter_lists(
                            api_path_level_parameters,
                            operation_level_parameters,
                        ),
                        in_=PATH,
                    )

                    for parameter in parameters_in_path:
                        if parameter['name'] not in path_parameter_names:
                            key = "{method}:{api_path}".format(
                                method=method.upper(),
                                api_path=api_path,
                            )
                            errors[key].add_error(
                                MESSAGES["path"]["missing_parameter"].format(
                                    parameter['name'], api_path,
                                ),
                            )

        return super(PathsSerializer, self).validate(attrs)

    def create(self, validated_data):
        return validated_data


class SwaggerSerializer(serializers.Serializer):
    """
    Primary Serializer for swagger schema
    """
    swagger = serializers.ChoiceField(
        choices=[
            ('2.0', '2.0'),
        ],
    )
    info = InfoSerializer()
    host = serializers.CharField(
        allow_null=True, required=False,
        validators=[host_validator],
    )
    basePath = serializers.CharField(
        allow_null=True, required=False,
        validators=[path_validator],
    )
    schemes = serializers.ListField(
        allow_null=True, required=False,
        child=serializers.CharField(
            allow_null=True, required=False, validators=[scheme_validator],
        ),
    )
    consumes = serializers.ListField(
        allow_null=True, required=False,
        child=serializers.CharField(
            allow_null=True, required=False, validators=[mimetype_validator],
        ),
    )
    produces = serializers.ListField(
        allow_null=True, required=False,
        child=serializers.CharField(
            allow_null=True, required=False, validators=[mimetype_validator],
        ),
    )

    paths = PathsSerializer()

    security = SecuritySerializer(allow_null=True, required=False)

    tags = TagSerializer(allow_null=True, required=False, many=True)
    externalDocs = serializers.CharField(allow_null=True, required=False)

    def update(self, instance, validated_data):
        instance.update(validated_data)
        return instance

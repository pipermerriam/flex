from __future__ import unicode_literals

import functools
import six

from rest_framework import serializers

from drf_compound_fields.fields import ListField

from flex.exceptions import (
    ValidationError,
    ErrorDict,
)
from flex.context_managers import ErrorCollection
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
    description = serializers.CharField(required=False)
    termsOfService = serializers.CharField(required=False)
    contact = serializers.CharField(required=False)
    license = serializers.CharField(required=False)
    version = serializers.CharField(required=False)


class ItemsSerializer(BaseItemsSerializer):
    default_error_messages = {
        'unknown_reference': 'Unknown definition reference `{0}`',
    }

    def from_native(self, data, files):
        if isinstance(data, six.string_types):
            definitions = self.context.get('definitions', {})
            if data not in definitions:
                raise ValidationError(
                    MESSAGES['unknown_reference']['definition'].format(data),
                )
            return data
        return super(ItemsSerializer, self).from_native(data, files)


class HeaderSerializer(BaseHeaderSerializer):
    items = ItemsSerializer(required=False, many=True)


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

    def save_object(self, obj, **kwargs):
        validators = construct_schema_validators(obj, self.context)
        self.object = functools.partial(validate_object, validators=validators)


class ResponseSerializer(BaseResponseSerializer):
    """
    https://github.com/wordnik/swagger-spec/blob/master/versions/2.0.md#responseObject
    """
    schema = SchemaSerializer(required=False)
    headers = HeadersSerializer(required=False)
    # TODO: how do we do examples
    # examples =


class ResponsesSerializer(HomogenousDictSerializer):
    value_serializer_class = ResponseSerializer


class SecuritySerializer(HomogenousDictSerializer):
    value_serializer_class = SecurityRequirementReferenceField


class ParameterSerializer(BaseParameterSerializer):
    schema = SchemaSerializer(required=False)
    items = ItemsSerializer(required=False, many=True)

    @property
    def many(self):
        return True

    @many.setter
    def many(self, value):
        pass

    def from_native(self, data, files=None):
        if isinstance(data, six.string_types):
            try:
                self.validate_reference(data)
            except ValidationError as err:
                assert not self._errors
                self._errors = err.messages
                return
            else:
                return data
        return super(ParameterSerializer, self).from_native(data, files)

    def validate_reference(self, reference):
        if reference not in self.context.get('parameters', {}):
            raise ValidationError(
                MESSAGES['unknown_reference']['parameter'].format(reference),
            )

    def save(self):
        return self.object


class OperationSerializer(serializers.Serializer):
    """
    https://github.com/wordnik/swagger-spec/blob/master/versions/2.0.md#operationObject
    """
    tags = ListField(required=False, validators=[string_type_validator])
    summary = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    externalDocs = serializers.CharField(required=False)
    operationId = serializers.CharField(required=False)
    consumes = ListField(required=False, validators=[mimetype_validator])
    produces = ListField(required=False, validators=[mimetype_validator])
    parameters = ParameterSerializer(required=False, many=True)
    responses = ResponsesSerializer()
    schemes = ListField(required=False, validators=[scheme_validator])
    deprecated = serializers.BooleanField(required=False)
    security = SecuritySerializer(required=False)


class PathItemSerializer(serializers.Serializer):
    """
    https://github.com/wordnik/swagger-spec/blob/master/versions/2.0.md#pathsObject
    """
    # TODO. reference path item objects from definitions.
    # TODO. how is this supposted to work.  The swagger spec doesn't account
    # for a definitions location for PathItem definitions?
    # _ref = serializers.CharField(source='$ref')
    get = OperationSerializer(required=False)
    put = OperationSerializer(required=False)
    post = OperationSerializer(required=False)
    delete = OperationSerializer(required=False)
    options = OperationSerializer(required=False)
    head = OperationSerializer(required=False)
    patch = OperationSerializer(required=False)
    # TODO: these can be a parameters reference object.
    parameters = ParameterSerializer(required=False, many=True)


class TagSerializer(serializers.Serializer):
    """
    https://github.com/wordnik/swagger-spec/blob/master/versions/2.0.md#tagObject
    """
    name = serializers.CharField()
    description = serializers.CharField(required=False)
    externalDocs = serializers.CharField(required=False)


class PropertiesSerializer(HomogenousDictSerializer):
    value_serializer_class = SchemaSerializer


# These fields include recursive use of the `SchemaSerializer` so they have to
# be attached after the `SchemaSerializer` class has been created.
SchemaSerializer.base_fields['properties'] = PropertiesSerializer(required=False)
SchemaSerializer.base_fields['items'] = ItemsSerializer(required=False, many=True)
SchemaSerializer.base_fields['allOf'] = SchemaSerializer(required=False, many=True)


class PathsSerializer(HomogenousDictSerializer):
    value_serializer_class = PathItemSerializer
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

    def save_object(self, obj, **kwargs):
        self.object = obj


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
        required=False,
        validators=[host_validator],
    )
    basePath = serializers.CharField(
        required=False,
        validators=[path_validator],
    )
    schemes = ListField(required=False, validators=[scheme_validator])
    consumes = ListField(required=False, validators=[mimetype_validator])
    produces = ListField(required=False, validators=[mimetype_validator])

    paths = PathsSerializer()

    security = SecuritySerializer(required=False)

    tags = TagSerializer(required=False, many=True)
    externalDocs = serializers.CharField(required=False)

    def save_object(self, obj, **kwargs):
        self.object = obj

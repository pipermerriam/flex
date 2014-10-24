import collections

import six

from rest_framework import serializers

from flex.serializers.common import (
    HomogenousDictSerializer,
    BaseResponseSerializer,
    BaseSchemaSerializer,
    BaseParameterSerializer,
    BaseItemsSerializer,
)
from flex.serializers.validators import (
    security_type_validator,
    security_api_key_location_validator,
    security_flow_validator,
)
from flex.constants import (
    API_KEY,
    OAUTH_2,
    IMPLICIT,
    PASSWORD,
    APPLICATION,
    ACCESS_CODE,
)


class SchemaSerializer(BaseSchemaSerializer):
    def from_native(self, data, files=None):
        if '$ref' in data:
            self.context['deferred_references'].add(data['$ref'])
        return super(SchemaSerializer, self).from_native(data, files)


class DefinitionsSerializer(HomogenousDictSerializer):
    default_error_messages = {
        'unknown_references': "Unknown references `{0}`",
    }

    value_serializer_class = SchemaSerializer

    def validate(self, attrs):

        deferred_references = self.context.get('deferred_references', set())
        missing_references = deferred_references.difference(attrs.keys())
        if missing_references:
            raise serializers.ValidationError(
                self.error_messages['unknown_references'].format(
                    list(missing_references),
                ),
            )
        return super(DefinitionsSerializer, self).validate(attrs)


class PropertiesSerializer(HomogenousDictSerializer):
    value_serializer_class = SchemaSerializer


class ItemsSerializer(BaseItemsSerializer):
    def from_native(self, data, files=None):
        if isinstance(data, six.string_types):
            self.context['deferred_references'].add(data)
            return [data]
        return super(ItemsSerializer, self).from_native(data, files)


# These fields include recursive use of the `SchemaSerializer` so they have to
# be attached after the `SchemaSerializer` class has been created.
SchemaSerializer.base_fields['properties'] = PropertiesSerializer(required=False)
SchemaSerializer.base_fields['items'] = ItemsSerializer(required=False, many=True)
SchemaSerializer.base_fields['allOf'] = SchemaSerializer(required=False, many=True)


class ParameterSerializer(BaseParameterSerializer):
    schema = SchemaSerializer(required=False)
    items = ItemsSerializer(required=False, many=True)


class ParameterDefinitionsSerializer(HomogenousDictSerializer):
    value_serializer_class = ParameterSerializer


class ScopesSerializer(HomogenousDictSerializer):
    value_serializer_class = serializers.CharField


class SecuritySchemeSerializer(serializers.Serializer):
    """
    https://github.com/wordnik/swagger-spec/blob/master/versions/2.0.md#securityDefinitionsObject
    """
    default_error_messages = {
        'name_required': 'When type is "apiKey", "name" is required.',
        'in_required': 'When type is "apiKey", "in" is required.',
        'flow_required': 'When type is "oath2" flow is required.',
        'authorization_url_required': (
            'When type is "oath2" and flow is one of ("implicit", '
            '"accessCode"), "authorizationUrl" is required.'
        ),
        'token_url_required': (
            'When type is "oath2" and flow is one of ("password", '
            '"application", "accessCode"), "authorizationUrl" is required.'
        ),
    }
    type = serializers.CharField(validators=[security_type_validator])
    description = serializers.CharField(required=False)
    name = serializers.CharField(required=False)
    flow = serializers.CharField(
        required=False, validators=[security_flow_validator],
    )
    # TODO: support SHOULD clauses about these being in the form of a url.
    authorizationUrl = serializers.CharField(required=False)
    tokenUrl = serializers.CharField(required=False)

    scopes = ScopesSerializer(required=False)

    def validate(self, attrs):
        errors = collections.defaultdict(list)

        # apiKey validations
        if attrs['type'] == API_KEY:
            if 'name' not in attrs:
                errors['name'].append(
                    self.error_messages['name_required'],
                )
            if 'in' not in attrs:
                errors['in'].append(
                    self.error_messages['in_required'],
                )
        elif attrs['type'] == OAUTH_2:
            if 'flow' not in attrs:
                errors['flow'].append(
                    self.error_messages['flow_required'],
                )
            if attrs.get('flow') in (IMPLICIT, ACCESS_CODE):
                if 'authorizationUrl' not in attrs:
                    errors['authorizationUrl'].append(
                        self.error_messages['authorization_url_required'],
                    )
            if attrs.get('flow') in (PASSWORD, APPLICATION, ACCESS_CODE):
                if 'tokenUrl' not in attrs:
                    errors['tokenUrl'].append(
                        self.error_messages['token_url_required'],
                    )

        if errors:
            raise serializers.ValidationError(errors)
        return super(SecuritySchemeSerializer, self).validate(attrs)


SecuritySchemeSerializer.base_fields['in'] = serializers.CharField(
    required=False,
    validators=[security_api_key_location_validator],
)


class SecurityDefinitionsSerializer(HomogenousDictSerializer):
    value_serializer_class = SecuritySchemeSerializer


class ResponseSerializer(BaseResponseSerializer):
    """
    https://github.com/wordnik/swagger-spec/blob/master/versions/2.0.md#responseObject
    """
    pass


class ResponseDefinitionsSerializer(HomogenousDictSerializer):
    value_serializer_class = ResponseSerializer


class SwaggerDefinitionsSerializer(serializers.Serializer):
    """
    Step 1 in the schema validation process is to gather all of the
    definitions.
    """
    def __init__(self, *args, **kwargs):
        context = kwargs.pop('context', {})
        context['deferred_references'] = set()
        kwargs['context'] = context
        super(SwaggerDefinitionsSerializer, self).__init__(*args, **kwargs)

    definitions = DefinitionsSerializer(required=False)
    parameters = ParameterDefinitionsSerializer(required=False)
    securityDefinitions = SecurityDefinitionsSerializer(required=False)
    responses = ResponseDefinitionsSerializer(required=False)

    def validate(self, attrs):
        deferred_references = self.context['deferred_references']
        missing_references = set()
        for deferred_reference in deferred_references:
            for definitions in attrs.values():
                if deferred_reference in definitions:
                    break
            else:
                missing_references.add(deferred_reference)
        if missing_references:
            raise serializers.ValidationError(
                {'missing_references': list(missing_references)},
            )
        return super(SwaggerDefinitionsSerializer, self).validate(attrs)

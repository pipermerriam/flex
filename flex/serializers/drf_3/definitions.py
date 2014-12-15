import six

from rest_framework import serializers

from flex.exceptions import (
    ValidationError,
    ErrorDict,
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

from .common import (
    HomogenousDictSerializer,
    BaseResponseSerializer,
    BaseSchemaSerializer,
    BaseParameterSerializer,
    BaseItemsSerializer,
    BaseHeaderSerializer,
)


class SchemaSerializer(BaseSchemaSerializer):
    def to_internal_value(self, data):
        if isinstance(data, six.string_types):
            self.context['deferred_references'].add(data)
            return data
        elif '$ref' in data:
            self.context['deferred_references'].add(data['$ref'])
        return super(SchemaSerializer, self).to_internal_value(data)


class DefinitionsSerializer(HomogenousDictSerializer):
    default_error_messages = {
        'unknown_references': "Unknown references `{0}`",
    }

    value_serializer_class = SchemaSerializer

    def validate(self, attrs):
        deferred_references = self.context.get('deferred_references', set())
        missing_references = deferred_references.difference(attrs.keys())
        if missing_references:
            raise ValidationError(
                self.error_messages['unknown_references'].format(
                    list(missing_references),
                ),
            )
        return super(DefinitionsSerializer, self).validate(attrs)

    def create(self, validated_data):
        return validated_data


class PropertiesSerializer(HomogenousDictSerializer):
    value_serializer_class = SchemaSerializer


class ItemsSerializer(BaseItemsSerializer):
    def run_validation(self, data):
        if isinstance(data, six.string_types):
            value = self.to_internal_value(data)
            return value
        return super(ItemsSerializer, self).run_validation(data)

    def to_internal_value(self, data):
        if isinstance(data, six.string_types):
            self.context['deferred_references'].add(data)
            return data
        return super(ItemsSerializer, self).to_internal_value(data)


# These fields include recursive use of the `SchemaSerializer` so they have to
# be attached after the `SchemaSerializer` class has been created.
SchemaSerializer._declared_fields['properties'] = PropertiesSerializer(required=False)
SchemaSerializer._declared_fields['items'] = ItemsSerializer(required=False, many=True)
SchemaSerializer._declared_fields['allOf'] = SchemaSerializer(required=False, many=True)


class HeaderSerializer(BaseHeaderSerializer):
    items = ItemsSerializer(required=False, many=True)
    schema = SchemaSerializer(required=False)


class HeadersSerializer(HomogenousDictSerializer):
    """
    https://github.com/wordnik/swagger-spec/blob/master/versions/2.0.md#headersObject
    """
    value_serializer_class = HeaderSerializer


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
        errors = ErrorDict()

        # apiKey validations
        if attrs['type'] == API_KEY:
            if 'name' not in attrs:
                errors['name'].add_error(
                    self.error_messages['name_required'],
                )
            if 'in' not in attrs:
                errors['in'].add_error(
                    self.error_messages['in_required'],
                )
        elif attrs['type'] == OAUTH_2:
            if 'flow' not in attrs:
                errors['flow'].add_error(
                    self.error_messages['flow_required'],
                )
            if attrs.get('flow') in (IMPLICIT, ACCESS_CODE):
                if 'authorizationUrl' not in attrs:
                    errors['authorizationUrl'].add_error(
                        self.error_messages['authorization_url_required'],
                    )
            if attrs.get('flow') in (PASSWORD, APPLICATION, ACCESS_CODE):
                if 'tokenUrl' not in attrs:
                    errors['tokenUrl'].add_error(
                        self.error_messages['token_url_required'],
                    )

        if errors:
            raise ValidationError(errors)
        return super(SecuritySchemeSerializer, self).validate(attrs)


SecuritySchemeSerializer._declared_fields['in'] = serializers.CharField(
    required=False,
    validators=[security_api_key_location_validator],
)


class SecurityDefinitionsSerializer(HomogenousDictSerializer):
    value_serializer_class = SecuritySchemeSerializer


class ResponseSerializer(BaseResponseSerializer):
    """
    https://github.com/wordnik/swagger-spec/blob/master/versions/2.0.md#responseObject
    """
    schema = SchemaSerializer(required=False)
    headers = HeadersSerializer(required=False)
    # example  # TODO: how do we do example.


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
            raise ValidationError(
                {'missing_references': list(missing_references)},
            )
        return super(SwaggerDefinitionsSerializer, self).validate(attrs)

    def create(self, validated_data):
        return validated_data

    def update(self, instance, validated_data):
        instance.update(validated_data)
        return instance

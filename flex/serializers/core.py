__all__ = [
    'SwaggerSerializer',
    'SchemaSerializer',
    'PathsSerializer',
    'ParameterSerializer',
    'HeaderSerializer',
]


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
"""

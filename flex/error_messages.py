from __future__ import unicode_literals


TYPE_MESSAGES = {
    'unknown': 'Unknown type: {0}',
    'invalid': "Got value `{0}` of type `{1}`.  Value must be of type(s): `{2}`",
    'invalid_header_type': (
        "Invalid type for header: `{0}`.  Must be one of 'string', 'number', "
        "'integer', 'boolean', or 'array'."
    ),
}

FORMAT_MESSAGES = {
    'invalid': "Value {0} does not conform to the format {1}",
    'invalid_uuid': "{0} is not a valid uuid",
    'invalid_datetime': "{0} is not a valid iso8601 date-time",
    'too_many_bits': "Integer {0} has {1} bits.  Must be no more than {2} bits",
    'invalid_uri': "The value `{0}` is not valid according to RFC3987.",
    'invalid_email': "The email address `{0}` is invalid according to RFC5322.",
}

REQUIRED_MESSAGES = {
    'required': "This value is required",
}

MULTIPLE_OF_MESSAGES = {
    'invalid': "Value must be a multiple of {0}.  Got {1} which is not.",
}

MINIMUM_AND_MAXIMUM_MESSAGES = {
    'invalid': "{0} must be {1} than {2}",
}


MIN_ITEMS_MESSAGES = {
    'invalid': "Array must have at least {0} items.  It had only had {1} items.",
}


MAX_ITEMS_MESSAGES = {
    'invalid': "Array must have no more than {0} items.  It had {1} items.",
}


UNIQUE_ITEMS_MESSAGES = {
    'invalid': "Array items must be unique.  The following items appeard more than once: {0}",
}


ENUM_MESSAGES = {
    'invalid': "Invalid value.  {0} is not one of the available options ({1})",
}


PATTERN_MESSAGES = {
    'invalid': "{0} did not match the pattern `{1}`.",
}


MIN_PROPERTIES_MESSAGES = {
    'invalid': "Object must have more than {0} properties.  It had {1}",
}


MAX_PROPERTIES_MESSAGES = {
    'invalid': "Object must have less than {0} properties.  It had {1}",
}


ITEMS_MESSAGES = {
    'invalid_type': '`items` must be a reference, a schema, or an array of schemas.',
}


REQUEST_MESSAGES = {
    'invalid_method': (
        'Request was not one of the allowed request methods.  Got '
        '`{0}`: Expected one of: `{1}`'
    ),
}


RESPONSE_MESSAGES = {
    'invalid_status_code': (
        "Request status code was not found in the known response codes.  Got "
        "`{0}`: Expected one of: `{1}`"
    )
}


PATH_MESSAGES = {
    'unknown_path': 'Request path did not match any of the known api paths.',
    'missing_parameter': (
        "The parameter named `{0}` is declared to be a PATH parameter but does "
        "not appear in the api path `{1}`.  All path parameters must exist as a "
        "parameter in the api path"
    )
}


UNKNOWN_REFERENCE_MESSAGES = {
    'security': "Unknown SecurityScheme reference `{0}`",
    'parameter': "Unknown Parameter reference `{0}`",
    'definition': 'Unknown definition reference `{0}`',
}


CONTENT_TYPE_MESSAGES = {
    'invalid': 'Invalid content type `{0}`.  Must be one of `{1}`.',
}


MESSAGES = {
    'type': TYPE_MESSAGES,
    'format': FORMAT_MESSAGES,
    'required': REQUIRED_MESSAGES,
    'multiple_of': MULTIPLE_OF_MESSAGES,
    'minimum': MINIMUM_AND_MAXIMUM_MESSAGES,
    'maximum': MINIMUM_AND_MAXIMUM_MESSAGES,
    'min_items': MIN_ITEMS_MESSAGES,
    'max_items': MAX_ITEMS_MESSAGES,
    'min_properties': MIN_PROPERTIES_MESSAGES,
    'max_properties': MAX_PROPERTIES_MESSAGES,
    'unique_items': UNIQUE_ITEMS_MESSAGES,
    'enum': ENUM_MESSAGES,
    'pattern': PATTERN_MESSAGES,
    'items': ITEMS_MESSAGES,
    'request': REQUEST_MESSAGES,
    'response': RESPONSE_MESSAGES,
    'path': PATH_MESSAGES,
    'unknown_reference': UNKNOWN_REFERENCE_MESSAGES,
    'content_type': CONTENT_TYPE_MESSAGES,
}

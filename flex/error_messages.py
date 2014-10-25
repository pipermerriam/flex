TYPE_MESSAGES = {
    'invalid': "Got value `{0}` of type `{1}`.  Value must be of type(s): `{2}`",
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


REQUEST_MESSAGES = {
    'unknown_path': 'Request path did not match any of the known api paths.',
    'invalid_method': (
        'Request status code was not found in the known response codes.  Got '
        '`{0}`: Expected one of: `{1}`'
    ),
}


RESPONSE_MESSAGES = {
    'invalid_status_code': (
        "Request status code was not found in the known response codes.  Got "
        "`{0}`: Expected one of: `{1}`"
    )
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
    'unique_items': UNIQUE_ITEMS_MESSAGES,
    'enum': ENUM_MESSAGES,
    'pattern': PATTERN_MESSAGES,
    'request': REQUEST_MESSAGES,
    'response': RESPONSE_MESSAGES,
}

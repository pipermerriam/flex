from __future__ import unicode_literals

import numbers
import collections
import six


SCHEMES = (
    'http', 'https', 'ws', 'wss',
)


MIMETYPES = (
    'application/json',
)


FORMATS = (
    ('integer', 'int32'),
    ('integer', 'int64'),
    ('number', 'float'),
    ('number', 'double'),
    ('string', 'byte'),
    ('string', 'date'),
    ('string', 'date-time'),
    ('string', 'email'),
    ('string', 'uri'),
)


NULL = 'null'
BOOLEAN = 'boolean'
INTEGER = 'integer'
NUMBER = 'number'
STRING = 'string'
ARRAY = 'array'
OBJECT = 'object'

PRIMATIVE_TYPES = {
    None: (type(None),),
    NULL: (type(None),),
    BOOLEAN: (bool,),
    INTEGER: (int,),
    NUMBER: (numbers.Number,),
    STRING: six.string_types,
    ARRAY: (collections.Sequence,),
    OBJECT: (collections.Mapping,),
}

HEADER_TYPES = (
    STRING,
    NUMBER,
    BOOLEAN,
    ARRAY,
    OBJECT,
)


PATH = 'path'
BODY = 'body'
QUERY = 'query'
FORM_DATA = 'formData'
HEADER = 'header'
PARAMETER_IN_VALUES = (
    QUERY,
    HEADER,
    PATH,
    FORM_DATA,
    BODY,
)


CSV = 'csv'
MULTI = 'multi'

COLLECTION_FORMATS = (
    CSV,
    'ssv',
    'tsv',
    'pipes',
    MULTI,
)


API_KEY = 'apiKey'
BASIC = 'basic'
OAUTH_2 = 'oath2'
SECURITY_TYPES = (
    API_KEY,
    BASIC,
    OAUTH_2,
)


QUERY = QUERY
HEADER = HEADER
SECURITY_API_KEY_LOCATIONS = (
    QUERY,
    HEADER,
)


IMPLICIT = 'implicit'
PASSWORD = 'password'
APPLICATION = 'application'
ACCESS_CODE = 'accessCode'
SECURITY_FLOWS = (
    IMPLICIT,
    PASSWORD,
    APPLICATION,
    ACCESS_CODE,
)


class Empty(object):
    def __cmp__(self, other):
        raise TypeError('Empty cannot be compared to other values')


"""
Sentinal empty value for use with distinguishing `None` from a key not
being present.
"""
EMPTY = Empty()

.. Flex documentation master file, created by
   sphinx-quickstart on Thu Oct 16 20:43:24 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Flex
====

Flex is a Swagger 2.0 validator.  It is currently at a very early stage in
development and thus is likely to have plenty of bugs.


General Use
-----------

install ``flex``

.. code-block:: shell

   $ pip install flex


Then in your code.

.. code-block:: python

   import flex

   schema = flex.load('path/to/schema.yaml')


Supported Schema Formats
------------------------

The ``flex.load`` function supports the following.

- A url to either a ``json`` or ``yaml`` schema.
- A path to either a ``json`` or ``yaml`` schema.
- A file object whose contents are ``json`` or ``yaml``
- A string whose contents are ``json`` or ``yaml``
- A native python object that is a ``Mapping`` (like a dictionary).


JSON Schema Validation
----------------------

A subset of the ``flex`` tooling implements JSON schema validation.

.. code-block:: python

   >>>  from flex.core import validate
   >>>  schema = {
   ...:   'properties': {
   ...:     'name': {
   ...:       'type': 'string',
   ...:       'minLength': 3,
   ...:     },
   ...:     'age': {
   ...:       'type': 'integer',
   ...:       'minimum': 0,
   ...:       'exclusiveMinimum': True,
   ...:     },
   ...:   }
   ...: }
   >>>  data = {
   ...:   'age': 10,
   ...:   'name': "John",
   ...: }
   >>>  validate(schema, data)
   >>>  bad_data = {
   ...:   'age': -5,
   ...:   'name': "Bo",
   ...: }
   >>>  validate(schema, bad_data)
   ValueError: Invalid:
   'age':
       - 'minimum':
           - u'-5 must be greater than than 0.0'
   'name':
       - 'minLength':
           - u'Ensure this value has at least 3 characters (it has 2).'


You can also use this to simply validate that your JSON schema conforms to
specification.

.. code-block:: python

   >>>  from flex.core import validate
   >>>  schema = {
   ...:   'properties': {
   ...:     'name': {
   ...:       'type': 'string',
   ...:       'minLength': 3,
   ...:     },
   ...:     'friends': {
   ...:       'type': 'array',
   ...:       'minimum': 0,  # `minimum` is invalid for type 'array'
   ...:     },
   ...:   }
   ...: }
   >>>  validate(schema)
   ValueError: JSON Schema did not validate:
   
   u'properties':
       - 'friends':
           - 'minimum':
               - u'`minimum` can only be used for json number types'

Response Validation
-------------------

Response validation takes a supported response object that represents a
request/response cycle for an API call and validates it against a swagger
schema.

.. code-block:: python

   >>> import requests
   >>> from flex.core import load, ResponseValidator
   >>> schema = load("path/to/schema.yaml")
   >>> validator = ResponseValidator(schema)
   >>> response = requests.get('http://www.example.com/api/')
   >>> validator(response)
   ValueError: Invalid
   'response':
       - 'Request status code was not found in the known response codes.  Got `301`: Expected one of: `[200]`'


Response validation does the following steps.

1. Matches the request path to the appropriate api path.
2. Validate the request method.
3. Validate the request parameters (currently path, query, and header).
4. Validate the response status code.
5. Validate the response body.

The following validation is not yet implemented.

- Parameter validation for Form Data, and Body parameters.
- Response header validation.

Currently, response validation only supports response objects from the
``requests`` library.


Formats
-------

Flex implements format validation for the following formats

* ``uuid``:
  Version 1, 3, 4, and 5
* ``datetime``:
  iso8601 formatted datetimes via https://pypi.python.org/pypi/iso8601.
* ``int32``:
  Integers up to 32 bits.
* ``int64``:
  Integers up to 64 bits.
* ``email``:
  via https://pypi.python.org/pypi/validate_email
* ``uri``:
  via https://pypi.python.org/pypi/rfc3987

Flex supports registering your own custom formats for validation.


.. code-block:: python

   >>> from flex.formats import register
   >>> @register('title-case', 'string')
   ... def title_case_format_validator(value):
   ...     if not value == value.title():
   ...         raise ValidationError("Must be title cased")


In the example above, we have registered a new format ``title-case`` which is
applicatble to values of type string.  A validator function needs to take a
single value and raise a ``ValidationError`` if the value is invalid.

The ``register`` decorator takes the name of the format as it's first argument,
and then the remaining arguments should be the types that the format validator
can apply to.

.. note::
   Take note that format validation is skipped if the value is not of one of
   the specified types the format validator is declared for.

Command line usage
------------------

As well as a python API, ``flex`` also provides a commandline validation tool.

.. code-block:: bash
    $ ./flex -s /path/to/swagger.yaml
    $ ./flex -s http://spec.example.com/swagger.yaml


In the event of a validation error, the commandline program will return 1 and 
print to stderr a list of the validation errors detected.

If the file passes validation it will return to stdout "Validation passed" and return
0 - in line with most *nix commandline tools*.


Contents:

.. toctree::
   :maxdepth: 2


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

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


Supported Formats
-----------------

The ``flex.load`` function supports the following.

- A path to either a ``json`` or ``yaml`` file.
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


Contents:

.. toctree::
   :maxdepth: 2


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

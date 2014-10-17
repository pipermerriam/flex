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


Contents:

.. toctree::
   :maxdepth: 2



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


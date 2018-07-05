======
middle
======

``middle`` is a flexible, extensible Python data structures for general usage. Get data in and out, reliably, without boilerplate and with speed!

The most simple example of ``middle`` and some of its features:

.. code-block:: pycon

    >>> import typing
    >>> import middle

    >>> class Address(middle.Model):
    ...     street_name: str
    ...     number: typing.Optional[int]
    ...     city: str

    >>> class Person(middle.Model):
    ...     name: str
    ...     age: int
    ...     city: typing.Dict[str, Address]

    >>> data = {
    ...     "name": "John Doe",
    ...     "age": 42,
    ...     "address": {
    ...         "home": {
    ...             "street_name": "Foo St",
    ...             "number": None,
    ...             "city": "Python Park"
    ...         },
    ...         "work": {
    ...             "street_name": "Bar Blvd",
    ...             "number": "1337",
    ...             "city": "Park City"
    ...         }
    ...     }
    ... }

    >>> person = Person(data)

    >>> person
    Person(name='John Doe', age=42, address={'home': Address(street_name='Foo St', number=None, city='Python Park'), 'work': Address(street_name='Bar Blvd', number=1337, city='Park City')})

    >>> middle.asdict(person)
    {'name': 'John Doe', 'age': 42, 'address': {'home': {'street_name': 'Foo St', 'number': None, 'city': 'Python Park'}, 'work': {'street_name': 'Bar Blvd', 'number': 1337, 'city': 'Park City'}}}

Check more about ``middle`` features:

------------

.. toctree::
   :maxdepth: 1
   :caption: Contents:

   about
   installation
   usage
   types
   validators
   configuration
   attrs
   extending
   troubleshooting
   reference/index
   contributing
   authors
   changelog

------------

Quick links
-----------

* `Source code <https://github.com/vltr/middle>`_
* `Issues <https://github.com/vltr/middle/issues>`_

======
middle
======

Flexible, extensible Python data structures for general usage. Get data in and out, reliably, without boilerplate and with speed!

``middle`` stands on the shoulders of ``attrs`` and aims to be as simple as possible to get data from complex objects to Python primitives and vice-versa, with validators, converters, a lot of sugar and other utilities! ``middle`` can be used with your preferred web framework, background job application, configuration parser and more!


Quick peak
----------

The most simple example of ``middle`` and some of its features (using Python 3.6+ syntax):

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
    ...     address: typing.Dict[str, Address]

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

Wanted a more complex example, with Python 3.5 compatible syntax? For sure!

.. code-block:: pycon

    >>> from typing import Dict, List
    >>> import middle

    >>> class Game(middle.Model):
    ...     name = middle.field(type=str)
    ...     score = middle.field(type=float, minimum=0, maximum=10)
    ...     resolution_tested = middle.field(type=str, pattern="^\d+x\d+$")
    ...     genre = middle.field(type=List[str], unique_items=True)
    ...     rating = middle.field(type=Dict[str, float], max_properties=5)

    >>> data = {
    ...     "name": "Cities: Skylines",
    ...     "score": 9.0,
    ...     "resolution_tested": "1920x1200",
    ...     "genre": ["Simulators", "City Building"],
    ...     "rating": {
    ...         "IGN": 8.5,
    ...         "Gamespot": 8.0,
    ...         "Steam": 4.5
    ...     }
    ... }

    >>> game = Game(**data)

    >>> game
    Game(name='Cities: Skylines', score=9.0, resolution_tested='1920x1200', genre=['Simulators', 'City Building'], rating={'IGN': 8.5, 'Gamespot': 8.0, 'Steam': 4.5})

    >>> middle.asdict(game)
    {'name': 'Cities: Skylines', 'score': 9.0, 'resolution_tested': '1920x1200', 'genre': ['Simulators', 'City Building'], 'rating': {'IGN': 8.5, 'Gamespot': 8.0, 'Steam': 4.5}}


``middle`` is flexible enough to understand ``Enum``, nested models and a large variety of types declared on the ``typing`` module out of the box. Also, you can :ref:`extend it <extending>` to your own classes!

.. warning::

    **IMPORTANT**: ``middle`` is in **very early stages** of development. There's a lot of functionalities that needs to be implemented and some known misbehaviors to be addressed, not to mention it needs a lot of testing before moving to any other status rather than **alpha**.

----------

.. toctree::
    :caption: Starting with middle
    :maxdepth: 1

    about
    installing
    usage
    types

.. toctree::
    :caption: Advanced topics
    :maxdepth: 1

    validating
    configuring
    extending
    attrs
    troubleshooting

.. toctree::
    :caption: About the Project
    :maxdepth: 2

    reference/index
    contributing
    changelog
    authors


Useful links
------------

* `Source code <https://github.com/vltr/middle>`_
* `Issues <https://github.com/vltr/middle/issues>`_


Inspirations and thanks
-----------------------

Some libs that inspired the creation of ``middle``:

- `attrs <http://www.attrs.org/en/stable/>`_: how such a simple library can be such flexible, extendable and fast?
- `cattrs <https://github.com/Tinche/cattrs>`_: for its speed on creating ``attrs`` instances from ``dict`` and to instances again;
- `pydantic <https://pydantic-docs.helpmanual.io/>`_: for such pythonic and beautiful approach on creating classes using ``typing`` hints;
- `mashmallow <https://marshmallow.readthedocs.io/en/latest/>`_: it is one of the most feature rich modelling APIs I've seen;
- `apistar <https://docs.apistar.com/>`_: it's almost magical!
- `Sanic <http://sanic.readthedocs.io/en/latest/>`_: "*Gotta go fast!*"
- `ionelmc/cookiecutter-pylibrary <https://github.com/ionelmc/cookiecutter-pylibrary>`_: The most complete (or interesting) ``cookiecutter`` template I found so far (make sure to `read this <https://blog.ionelmc.ro/2014/05/25/python-packaging/>`_ article too);

License
-------

``middle`` is a free software distributed under the `MIT <https://choosealicense.com/licenses/mit/>`_ license.

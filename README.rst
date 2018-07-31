==========
``middle``
==========

.. start-badges

.. image:: https://img.shields.io/pypi/status/middle.svg
    :alt: PyPI - Status
    :target: https://pypi.org/project/middle/

.. image:: https://img.shields.io/pypi/v/middle.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/middle/

.. image:: https://img.shields.io/pypi/pyversions/middle.svg
    :alt: Supported versions
    :target: https://pypi.org/project/middle/

.. image:: https://travis-ci.org/vltr/middle.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/vltr/middle

.. image:: https://ci.appveyor.com/api/projects/status/github/vltr/middle?branch=master&svg=true
    :alt: AppVeyor Build Status
    :target: https://ci.appveyor.com/project/vltr/middle

.. image:: https://readthedocs.org/projects/middle/badge/?style=flat
    :target: https://readthedocs.org/projects/middle
    :alt: Documentation Status

.. image:: https://codecov.io/github/vltr/middle/coverage.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/vltr/middle

.. image:: https://api.codacy.com/project/badge/Grade/10c6ef32dfbe497087d57c9d86c02c80
    :alt: Codacy Grade
    :target: https://www.codacy.com/app/vltr/middle?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=vltr/middle&amp;utm_campaign=Badge_Grade

.. image:: https://pyup.io/repos/github/vltr/middle/shield.svg
    :target: https://pyup.io/account/repos/github/vltr/middle/
    :alt: Packages status

.. end-badges

Flexible, extensible Python data structures for general usage. Get data in and out, reliably, without boilerplate and with speed!

``middle`` stands on the shoulders of ``attrs`` and aims to be as simple as possible to get data from complex objects to Python primitives and vice-versa, with validators, converters, a lot of sugar and other utilities! ``middle`` can be used with your preferred web framework, background job application, configuration parser and more!

Sneak peek
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
    ...     name: str = middle.field()
    ...     score: float = middle.field(minimum=0, maximum=10)
    ...     resolution_tested: str = middle.field(pattern="^\d+x\d+$")
    ...     genre: List[str] = middle.field(unique_items=True)
    ...     rating: Dict[str, float] = middle.field(max_properties=5)

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


``middle`` is flexible enough to understand ``Enum``, nested models and a large variety of types declared on the ``typing`` module out of the box. Also, you can `extend it <https://middle.readthedocs.io/en/latest/extending.html>`_ to your own classes!

.. warning::

    **IMPORTANT**: ``middle`` is in **very early stages** of development. There are some requirements (like ``python-dateutil``) that would not be required in future releases; as there's a lot of functionalities that needs to be implemented and some known misbehaviors to be addressed, not to mention it needs a lot of testing before moving to any other status rather than **alpha**.

TODO
====

- Alias options (keys) to populate classes;
- Read-only and write-only fields;
- Better error handling (almost everywhere);
- Create a benchmark suite against other solutions;
- Formatters are still missing;
- Possibility to "cast" an instance to another instance where the original object is a subclass of it;

Done
----

- If possible, fine grain the converters, so a ``str`` input value of ``{}`` doesn't end up as ``str({})``;
- Get ``date`` and ``datetime`` converters to be customizable, instead of an ``if isinstance`` statement;
- Implement more validators and a registerable for more metadata options;
- Implement a better "type dispatcher" based on more complex rules (other than ``type(field.type)`` delivered by ``functools.singledispatch``) because the ``typing`` module has changed **a bit** between Python 3.6 and 3.7;
- Support more types (``typing.Tuple``, ``decimal.Decimal``);
- Get 100% (or closer) in code coverage;
- Lots of documentation;
- Python 3.5 support (with the exception of Windows platforms, see warning for Windows developers below);

Future discussions
------------------

- In Python 3.7, a neat feature was added: ``dataclasses``. I know it sounds really awesome to not depend on a 3rd-party library - such as ``attrs``, but the latest provides a lot of functionalities that can't be found on Python 3.7 ``dataclasses`` (for now), so I'll leave this open for further discussion.

Warning for Windows developers
------------------------------

If you're using Windows and Python 3.5, I think ``middle`` would not work well for you. CI in AppVeyor was disabled for Python 3.5 because of `this issue <https://github.com/python/typing/issues/523>`_. If Guido doesn't care, why should I (or you) ?

Documentation
=============

https://middle.readthedocs.io/en/latest/

Useful links
------------

* `Source code <https://github.com/vltr/middle>`_
* `Issues <https://github.com/vltr/middle/issues>`_

Inspirations and thanks
=======================

Some libs that inspired the creation of ``middle``:

- `attrs <http://www.attrs.org/en/stable/>`_: how such a simple library can be such flexible, extendable and fast?
- `cattrs <https://github.com/Tinche/cattrs>`_: for its speed on creating ``attrs`` instances from ``dict`` and to instances again;
- `pydantic <https://pydantic-docs.helpmanual.io/>`_: for such pythonic and beautiful approach on creating classes using ``typing`` hints;
- `mashmallow <https://marshmallow.readthedocs.io/en/latest/>`_: it is one of the most feature rich modelling APIs I've seen;
- `apistar <https://docs.apistar.com/>`_: it's almost magical!
- `Sanic <http://sanic.readthedocs.io/en/latest/>`_: "*Gotta go fast!*"
- `ionelmc/cookiecutter-pylibrary <https://github.com/ionelmc/cookiecutter-pylibrary>`_: The most complete (or interesting) ``cookiecutter`` template I found so far (make sure to `read this article <https://blog.ionelmc.ro/2014/05/25/python-packaging/>`_ too);

License
=======

``middle`` is a free software distributed under the `MIT <https://choosealicense.com/licenses/mit/>`_ license.

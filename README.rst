==========
``middle``
==========

.. start-badges

.. image:: https://readthedocs.org/projects/middle/badge/?style=flat
    :target: https://readthedocs.org/projects/middle
    :alt: Documentation Status

.. image:: https://travis-ci.org/vltr/middle.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/vltr/middle

.. image:: https://ci.appveyor.com/api/projects/status/github/vltr/middle?branch=master&svg=true
    :alt: AppVeyor Build Status
    :target: https://ci.appveyor.com/project/vltr/middle

.. image:: https://requires.io/github/vltr/middle/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/vltr/middle/requirements/?branch=master

.. image:: https://codecov.io/github/vltr/middle/coverage.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/vltr/middle

.. image:: https://img.shields.io/pypi/v/middle.svg
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/middle

.. image:: https://img.shields.io/github/commits-since/vltr/middle/v0.1.0.svg
    :alt: Commits since latest release
    :target: https://github.com/vltr/middle/compare/v0.1.0...master

.. image:: https://img.shields.io/pypi/wheel/middle.svg
    :alt: PyPI Wheel
    :target: https://pypi.python.org/pypi/middle

.. image:: https://img.shields.io/pypi/pyversions/middle.svg
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/middle

.. image:: https://img.shields.io/pypi/implementation/middle.svg
    :alt: Supported implementations
    :target: https://pypi.python.org/pypi/middle

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :alt: Code style: black
    :target: https://github.com/ambv/black

.. end-badges

Flexible, extensible Python data structures for general usage. Get data in and out, reliably, without boilerplate and with speed!

``middle`` stands on the shoulders of ``attrs`` and aims to be as simple as possible to get data from complex objects to Python primitives and vice-versa, with validators, converters and a lot of sugar! ``middle`` can be used with your preferred web framework, background job application, configuration parsing and many others!

.. code-block::pycon

    >>> from typing import Dict, List
    >>> import middle

    >>> class Game(middle.Model):
    ...     name: str = middle.field()
    ...     score: float = middle.field()
    ...     resolution_tested: str = middle.field(pattern="^\d+x\d+$")
    ...     genre: List[str] = middle.field()
    ...     rating: Dict[str, float] = middle.field()

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


``middle`` is flexible enough to understand ``Enum``, nested models and a large variety of types declared on the ``typing`` Python module out of the box. Also, you can extend it to your own classes!

.. warning::

    **IMPORTANT**: ``middle`` is in **very early stages** of development. There are some requirements (like ``python-dateutil`` and ``pytz``) that would not be required in future releases; as there's a lot of functionalities that needs to be implemented and some known misbehaviors to be addressed, not to mention it needs a lot of testing before moving to any other status rather than **pre-alpha** or **alpha**.

TODO
====

- Get 100% (or closer) in code coverage;
- Alias options to populate classes;
- Read-only and write-only fields;
- Better error handling (almost everywhere);
- If possible, fine grain the converters, so a ``str`` input value of ``{}`` doesn't end up as ``str({})``;
- Get ``date`` and ``datetime`` converters to be customizeable, instead of an ``if isinstance`` statement;
- Lots of documentation;
- More benchmarks;
- Support more types (provided in the Python standard library), if possible;

Documentation
=============

https://middle.readthedocs.io/

Inspiration and Thanks
======================

I really got inspired to create this library by observing a lot of other libraries and tools, specially:

- `attrs <http://www.attrs.org>`_: how such a simple library can be such flexible, extendable and fast?
- `cattrs <https://github.com/Tinche/cattrs>`_: for its speed on creating ``attrs`` instances from ``dicts`` and to instances again;
- `pydantic <https://pydantic-docs.helpmanual.io/>`_: for such pythonic and beautiful approach on creating classes using ``typing`` hints;
- `mashmallow <https://marshmallow.readthedocs.io/>`_: it is one of the most feature rich modelling APIs I've seen;
- `apistar <https://docs.apistar.com/>`_: it's almost magical!
- `Sanic <http://sanic.readthedocs.io/>`_: "*Gotta go fast!*"

License
=======

``middle`` is free software distributed under the `MIT <https://choosealicense.com/licenses/mit/>`_ license.

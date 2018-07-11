.. _about:

================
About ``middle``
================

``middle`` is a library created to provide a *pythonic* way to describe your data structures in the most simple way by using ``typing`` hints (from `PEP 484 <https://www.python.org/dev/peps/pep-0484/>`_), not only providing better readability but also all the necessary boilerplate to create objects based on your data structures, validate and customize input and output.

``middle`` is fast. Lightning fast. It can be used with your favourite web framework, background application, configuration parser or any other usage for highly customized input and/or output of primitive values.

.. important::

    ``middle`` was designed with ``typing`` hints in mind. It'll not work if no type is provided within your classes!

What to expect
--------------

``middle`` stands on the shoulders of ``attrs`` and aims to be as simple as possible to get data from complex objects to Python primitives and vice-versa.

As for "primitives", you can expect to have simple Python values (like ``list``, ``dict``, ``str``, ``int``, ``Enum`` and others) to convert from and to complex objects, containing even other nested objects from any type you can imagine (do not forget to read :ref:`how to extend <extending>` ``middle`` later on).

Another feature you can expect from ``middle`` is it speed. ``middle`` can convert from and to objects in a fraction of time compared to some of his "nearest" relatives, which makes it perfect if you need to handle lots of data. But you can use ``middle`` with any use case you (my dear friend developer) find fit, because it will do the job just fine.

Benchmarks
~~~~~~~~~~

(Sneaky) author took a copy of `pydantic benchmark suite <https://github.com/samuelcolvin/pydantic/tree/master/benchmarks>`_ and created a benchmark file for ``middle`` (mostly illustrative):

.. code-block:: python

    import typing
    from datetime import datetime

    import middle


    class TestMiddle:
        package = "middle"

        def __init__(self, allow_extra):
            class Location(middle.Model):
                latitude: float = middle.field(default=None)
                longitude: float = middle.field(default=None)

            class Skill(middle.Model):
                subject: str = middle.field()
                subject_id: int = middle.field()
                category: str = middle.field()
                qual_level: str = middle.field()
                qual_level_id: int = middle.field()
                qual_level_ranking: float = middle.field(default=0)

            class Model(middle.Model):
                id: int = middle.field()
                client_name: str = middle.field(max_length=255)
                sort_index: float = middle.field()
                grecaptcha_response: str = middle.field(
                    min_length=20, max_length=1000
                )
                client_phone: str = middle.field(max_length=255, default=None)
                location: Location = middle.field(default=None)
                contractor: int = middle.field(minimum=1, default=None)
                upstream_http_referrer: str = middle.field(
                    max_length=1023, default=None
                )
                last_updated: datetime = middle.field(default=None)
                skills: typing.List[Skill] = middle.field(default=[])

            self.model = Model

        def validate(self, data):
            try:
                return True, self.model(**data)
            except Exception as e:
                return False, str(e)

I must say that the results were really encouraging considering this is pure Python code (on an old AMD machine), no Cython, no Jit:

+--------------------------+--------------+----------+------------+
| Framework                | Comparison   | avg/iter | stdev/iter |
+==========================+==============+==========+============+
| middle (alpha)           |              | 39.1μs   | 0.186μs    |
+--------------------------+--------------+----------+------------+
| pydantic                 | 1.6x slower  | 62.4μs   | 0.278μs    |
+--------------------------+--------------+----------+------------+
| toasted-marshmallow      | 1.7x slower  | 64.9μs   | 0.352μs    |
+--------------------------+--------------+----------+------------+
| marshmallow              | 2.0x slower  | 79.3μs   | 0.137μs    |
+--------------------------+--------------+----------+------------+
| trafaret                 | 2.5x slower  | 97.7μs   | 1.586μs    |
+--------------------------+--------------+----------+------------+
| django-restful-framework | 17.0x slower | 662.8μs  | 1.649μs    |
+--------------------------+--------------+----------+------------+

.. warning::

    Keep in mind that ``middle`` is still in alpha stage. This benchmark will must likely change as ``middle`` evolves, since there are some features missing yet (to get to version 1.0.0).

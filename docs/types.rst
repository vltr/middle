.. _types:

===================
Types in ``middle``
===================

Typing hints (from `PEP 484 <https://www.python.org/dev/peps/pep-0484/>`_) are a major improvement to the Python language when dealing with documentation, code readability, `static <https://pyre-check.org/>`_ (and also `runtime <https://github.com/Instagram/MonkeyType>`_) code analysis **and**, in some cases, to provide extra logic to your code (which is, of course, the goal of ``middle``).

``middle`` supports a lot of builtin types, some from regularly used modules. There's also the possibility of :ref:`customize <extending>` ``middle`` to support many other types, including custom ones.

Supported types
---------------

- ``str``
- ``int``
- ``float``
- ``bool``
- ``bytes``
- ``datetime.date``
- ``datetime.datetime``
- ``decimal.Decimal``
- ``enum.Enum``
- ``typing.Dict``
- ``typing.List``
- ``typing.Set``
- ``typing.Tuple``
- ``typing.Union``
- ``typing.Collection``
- ``typing.Iterable``
- ``typing.Sequence``
- ``typing.MutableSequence``
- ``typing.FrozenSet``
- ``typing.MutableSet``
- ``typing.Mapping``
- ``typing.MutableMapping``

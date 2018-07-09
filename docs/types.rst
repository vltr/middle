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

``dict``, ``list``, ``set``
---------------------------

Since ``dict``, ``list`` and ``set`` can't have a distinguished type, they will not be supported by ``middle``. Instead, use ``typing.Dict``, ``typing.List`` and ``typing.Set``, respectively.

``datetime.date`` and ``datetime.datetime``
-------------------------------------------

For now, ``middle`` depends on two extra requirements to properly handle ``date`` and ``datetime`` objects, which are ``pytz`` and ``python-dateutil``, that are currently found on most Python projects already (that deals with this kind of value).

.. important::

    All naive ``datetime`` string or timestamp representations will be considered as UTC by ``middle``, thus any of this objects or representations that are not naive will remain untouched, but can be automatically converted to UTC for uniformity (see :ref:`configuration <configuration>`). Naive ``datetime`` objects will use the current machine timezone and can be converted to UTC for uniformity (also in :ref:`configuration <configuration>`).

.. warning::

    Even though the ``datetime`` API provides us two methods for getting the current date and time, ``now`` and ``utcnow``, both objects will be created **without** ``tzinfo``, making both instances **naive**. Basically, it means that no one can determine if a datetime object is not naive if the timezone is not explicitly provided:

    .. code-block:: pycon

        >>> from datetime import datetime

        >>> x = datetime.now()
        >>> x
        datetime.datetime(2018, 7, 9, 14, 21, 44, 624833)

        >>> x.tzinfo is None
        True

        >>> y = datetime.utcnow()
        >>> y
        datetime.datetime(2018, 7, 9, 17, 22, 12, 673103)

        >>> y.tzinfo is None
        True

    The `recomended way <https://docs.python.org/3/library/datetime.html#datetime.datetime.now>`_ to get an aware UTC datetime object would be:

    .. code-block:: pycon

        >>> from datetime import datetime, timezone

        >>> datetime.now(timezone.utc)
        datetime.datetime(2018, 7, 9, 17, 26, 8, 874805, tzinfo=datetime.timezone.utc)


Examples
~~~~~~~~

Considering a machine configured to GMT-0300 timezone at 10:30 AM local time:

.. code-block:: pycon

    >>> import datetime
    ... import pytz

    >>> from middle.dtutils import dt_convert_to_utc
    ... from middle.dtutils import dt_from_iso_string
    ... from middle.dtutils import dt_from_timestamp
    ... from middle.dtutils import dt_to_iso_string

    >>> dt_to_iso_string(datetime.datetime.now())
    '2018-07-09T10:30:00-03:00'

    >>> dt_to_iso_string(datetime.datetime.utcnow())
    '2018-07-09T13:30:00-03:00'

    >>> dt_from_iso_string("2018-07-02T08:30:00+01:00")
    datetime.datetime(2018, 7, 2, 8, 30, tzinfo=tzoffset(None, 3600))

    >>> dt_from_iso_string("2018-07-02T08:30:00")
    datetime.datetime(2018, 7, 2, 8, 30, tzinfo=datetime.timezone.utc)

    >>> dt_from_timestamp(1530520200)
    datetime.datetime(2018, 7, 2, 5, 30, tzinfo=datetime.timezone(datetime.timedelta(-1, 75600), '-03'))

    >>> dt_from_timestamp(1530520200.000123)
    datetime.datetime(2018, 7, 2, 5, 30, 0, 123, tzinfo=datetime.timezone(datetime.timedelta(-1, 75600), '-03'))

    >>> dt_convert_to_utc(datetime.datetime(2018, 7, 2, 8, 30, 0, 0, pytz.timezone("CET")))
    datetime.datetime(2018, 7, 2, 7, 30, tzinfo=<UTC>)

    >>> dt_convert_to_utc(dt_from_iso_string("2018-07-02T08:30:00+01:00"))
    datetime.datetime(2018, 7, 2, 7, 30, tzinfo=<UTC>)

One plus of using ``datetime`` in ``middle`` is that it accepts a wide range of inputs, having in mind that we're talking about Python here (see the ``datetime`` `constructor <https://docs.python.org/3/library/datetime.html#datetime.datetime>`_ to understand why):

.. code-block:: pycon

    >>> from datetime import datetime
    >>> import middle

    >>> class TestModel(middle.Model):
    ...     created_on: datetime = middle.field()

    >>> TestModel(created_on=datetime.now())
    TestModel(created_on=datetime.datetime(2018, 7, 9, 14, 36, 7, 679625, tzinfo=datetime.timezone(datetime.timedelta(-1, 75600), '-03')))

    >>> TestModel(created_on=datetime.now(timezone.utc))
    TestModel(created_on=datetime.datetime(2018, 7, 9, 17, 37, 35, 333771, tzinfo=datetime.timezone.utc))

    >>> TestModel(created_on="2018-7-7 4:42pm")
    TestModel(created_on=datetime.datetime(2018, 7, 7, 16, 42, tzinfo=datetime.timezone.utc))

    >>> TestModel(created_on=1530520200)
    TestModel(created_on=datetime.datetime(2018, 7, 2, 5, 30, tzinfo=datetime.timezone(datetime.timedelta(-1, 75600), '-03')))

    >>> TestModel(created_on=(2018, 7, 9, 10))
    TestModel(created_on=datetime.datetime(2018, 7, 9, 10, 0, tzinfo=datetime.timezone(datetime.timedelta(-1, 75600), '-03')))

    >>> TestModel(created_on=(2018, 7, 9, 10, 30, 0, 0, 1))
    TestModel(created_on=datetime.datetime(2018, 7, 9, 10, 30, tzinfo=datetime.timezone(datetime.timedelta(0, 3600))))

.. important::

    In the last input (in the example above), where a tuple of 8 integers were given for the ``created_on`` parameter, the last value corresponds to the **UTC offset in hours**.

Enum
----

Most enum types will be directly available from and to primitives by acessing the ``.value`` attribute of each instance. A lot of complex examples can work out of the box:

.. code-block:: pycon

    >>> import enum
    ... import middle

    >>> class AutoName(enum.Enum):
    ...     def _generate_next_value_(name, start, count, last_values):
    ...         return name

    >>> class TestAutoEnum(AutoName):
    ...     FOO = enum.auto()
    ...     BAR = enum.auto()
    ...     BAZ = enum.auto()

    >>> @enum.unique
    ... class TestStrEnum(str, enum.Enum):
    ...     CAT = "CAT"
    ...     DOG = "DOG"
    ...     BIRD = "BIRD"

    >>> @enum.unique
    ... class TestIntEnum(enum.IntEnum):
    ...     FIRST = 1
    ...     SECOND = 2
    ...     THIRD = 3

    >>> class TestFlagEnum(enum.IntFlag):
    ...     R = 4
    ...     W = 2
    ...     X = 1

    >>> instance = TestModel(auto_enum=TestAutoEnum.FOO, str_enum=TestStrEnum.CAT, int_enum=TestIntEnum.FIRST, flg_enum=TestFlagEnum.R | TestFlagEnum.W)
    >>> instance
    TestModel(auto_enum=<TestAutoEnum.FOO: 'FOO'>, str_enum=<TestStrEnum.CAT: 'CAT'>, int_enum=<TestIntEnum.FIRST: 1>, flg_enum=<TestFlagEnum.R|W: 6>)

    >>> data = middle.asdict(instance)
    >>> data
    {'auto_enum': 'FOO', 'str_enum': 'CAT', 'int_enum': 1, 'flg_enum': 6}

    >>> TestModel(**data)  # to test if flg_enum=6 would work
    TestModel(auto_enum=<TestAutoEnum.FOO: 'FOO'>, str_enum=<TestStrEnum.CAT: 'CAT'>, int_enum=<TestIntEnum.FIRST: 1>, flg_enum=<TestFlagEnum.R|W: 6>)

Future plans on types
---------------------

There are some types in the Python stdlib that are planned to be part of ``middle`` in the near future:

- uuid.uuid

If there's a type you would like to see on ``middle``, feel free to `open an issue <https://github.com/vltr/middle/issues>`_ or submit a PR.

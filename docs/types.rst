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

``dict``, ``list``, ``set``
---------------------------

Since ``dict``, ``list`` and ``set`` can't have a distinguished type, they will not be supported by ``middle``. Instead, use ``typing.Dict``, ``typing.List`` and ``typing.Set``, respectively.

``datetime.date`` and ``datetime.datetime``
-------------------------------------------

For now, ``middle`` depends on one extra requirements to properly handle ``date`` and ``datetime`` objects, which is ``python-dateutil`` (to properly format ``datetime`` string representations into ``datetime`` instances), and it is generally found on most Python projects / libraries already (that handles ``datetime`` string parsing).

.. important::

    All naive ``datetime`` string or timestamp representations will be considered as UTC (and converted accordingly) by ``middle``, thus any of this objects or representations that are not naive will be automatically converted to UTC for uniformity. Naive ``datetime`` objects will transit with the current machine timezone and converted to UTC for uniformity (this transition can be modified to be considered as UTC, see more about :ref:`configuring middle <configuring>`).

.. warning::

    Even though the ``datetime`` API provides us two methods for getting the current date and time, ``now`` and ``utcnow``, both instances will be created **without** ``tzinfo``, thus making them **naive**. Basically, it means that no one can determine if a datetime object is not naive if the timezone is not explicitly provided:

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
    '2018-07-10T13:30:00+00:00'

    >>> dt_to_iso_string(datetime.datetime.utcnow())
    '2018-07-10T16:30:00+00:00'

    >>> dt_from_iso_string("2018-07-02T08:30:00+01:00")
    datetime.datetime(2018, 7, 2, 7, 30, tzinfo=datetime.timezone.utc)

    >>> dt_from_iso_string("2018-07-02T08:30:00")
    datetime.datetime(2018, 7, 2, 8, 30, tzinfo=datetime.timezone.utc)

    >>> dt_from_timestamp(1530520200)
    datetime.datetime(2018, 7, 2, 8, 30, tzinfo=datetime.timezone.utc)

    >>> dt_from_timestamp(1530520200.000123)
    datetime.datetime(2018, 7, 2, 8, 30, 0, 123, tzinfo=datetime.timezone.utc)

    >>> dt_convert_to_utc(datetime.datetime(2018, 7, 2, 8, 30, 0, 0, pytz.timezone("CET")))
    datetime.datetime(2018, 7, 2, 7, 30, tzinfo=datetime.timezone.utc)

    >>> dt_convert_to_utc(dt_from_iso_string("2018-07-02T08:30:00+01:00"))
    datetime.datetime(2018, 7, 2, 7, 30, tzinfo=datetime.timezone.utc)

One plus of using ``datetime`` in ``middle`` is that it accepts a wide range of inputs, having in mind that we're talking about Python here (see the ``datetime`` `constructor <https://docs.python.org/3/library/datetime.html#datetime.datetime>`_ to understand why):

.. code-block:: pycon

    >>> from datetime import datetime, timezone
    >>> import middle

    >>> class TestModel(middle.Model):
    ...     created_on: datetime = middle.field()  # for Python 3.6+
    ...     created_on = middle.field(type=datetime)  # for Python 3.5

    >>> TestModel(created_on=datetime.now())
    TestModel(created_on=datetime.datetime(2018, 7, 10, 15, 1, 6, 121325, tzinfo=datetime.timezone.utc))

    >>> TestModel(created_on=datetime.now(timezone.utc))
    TestModel(created_on=datetime.datetime(2018, 7, 10, 15, 1, 40, 769369, tzinfo=datetime.timezone.utc))

    >>> TestModel(created_on="2018-7-7 4:42pm")
    TestModel(created_on=datetime.datetime(2018, 7, 7, 16, 42, tzinfo=datetime.timezone.utc))

    >>> TestModel(created_on=1530520200)
    TestModel(created_on=datetime.datetime(2018, 7, 2, 8, 30, tzinfo=datetime.timezone.utc))

    >>> TestModel(created_on=(2018, 7, 9, 10))
    TestModel(created_on=datetime.datetime(2018, 7, 9, 13, 0, tzinfo=datetime.timezone.utc))

    >>> TestModel(created_on=(2018, 7, 9, 10, 30, 0, 0, 1))
    TestModel(created_on=datetime.datetime(2018, 7, 9, 9, 30, tzinfo=datetime.timezone.utc))

.. important::

    In the last input (in the example above), where a tuple of 8 integers were given for the ``created_on`` parameter, the last value corresponds to the **UTC offset in hours**.

"But I only trust on [arrow|momentum|maya]"
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Well, I don't blame you. These operations regarding ``date`` and ``datetime`` were created for ``middle`` to provide an out-of-the-box solution for the most used types in Python, but, don't worry, you can override these operations with your own. Just head out to :ref:`extending <extending>` and catch up some examples.

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

- uuid.uuid[1,3-5]

If there's a type you would like to see on ``middle``, feel free to `open an issue <https://github.com/vltr/middle/issues>`_ or submit a PR.

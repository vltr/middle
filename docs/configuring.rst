.. _configuring:

===========
Configuring
===========

Configuring ``middle`` is straightforward, since it has just a few options, all of them regarding how the input data should be treated or converted when creating your models.

String input
------------

For an input string value, there are two options that can modify the way certain value can be turned into a ``str`` instance (or not).

``force_str``
~~~~~~~~~~~~~

**Default**: ``False``

By using ``force_str`` (as a ``bool``), every input value for ``str`` fields will be forced to use the ``str(value)`` function:

.. code-block:: pycon

    >>> import middle

    >>> class TestModel(middle.Model):
    ...     value = middle.field(type=str)

    >>> middle.config.force_str = True

    >>> TestModel(value=3.14)
    TestModel(value='3.14')

    >>> TestModel(value=object)
    TestModel(value="<class 'object'>")

``str_method``
~~~~~~~~~~~~~~

**Default**: ``True``

By using ``str_method`` (as a ``bool``), every input value for ``str`` fields will be checked for the existence of a ``__str__`` method and, if found, ``str(value)`` will be called:

.. code-block:: pycon

    >>> import middle

    >>> class TestModel(middle.Model):
    ...     value = middle.field(type=str)

    >>> TestModel(value=3.14)
    TestModel(value='3.14')

    >>> middle.config.str_method = False

    >>> TestModel(value=3.14)

.. code-block:: pytb

    Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
    File "/home/dev/middle/src/middle/model.py", line 105, in __call__
        return super().__call__(**kwargs)
    File "<attrs generated init b2f9a9c2c12524cd8fd8cd7557d4ba62494b3007>", line 2, in __init__
    File "/home/dev/.pyenv/versions/middle-3.6.6/lib/python3.6/site-packages/attr/converters.py", line 22, in optional_converter
        return converter(val)
    File "/home/dev/middle/src/middle/converters.py", line 46, in _str_converter
        'the value "{!s}" given should not be converted to str'.format(value)
    TypeError: the value "3.14" given should not be converted to str

Datetime input
--------------

``no_transit_local_dtime``
~~~~~~~~~~~~~~~~~~~~~~~~~~

**Default**: ``False``

By using ``no_transit_local_dtime`` (as a ``bool``), every datetime input value that doesn't have a timezone (naive instances) set will be treated as using the current machine timezone and automatically converted to UTC. If set to ``True``, all naive datetime instances will be already set as UTC. The examples bellow ran in a machine configured with the GMT-0300 timezone:

.. code-block:: pycon

    >>> from datetime import datetime
    >>> import middle

    >>> class TestModel(middle.Model):
    ...     value = middle.field(type=datetime)

    >>> TestModel(value=(2018, 7, 18, 14, 0))
    TestModel(value=datetime.datetime(2018, 7, 18, 17, 0, tzinfo=datetime.timezone.utc))

    >>> TestModel(value=datetime(2018, 7, 18, 14))
    TestModel(value=datetime.datetime(2018, 7, 18, 17, 0, tzinfo=datetime.timezone.utc))

    >>> TestModel(value="2018-07-18T14:00:00")
    TestModel(value=datetime.datetime(2018, 7, 18, 17, 0, tzinfo=datetime.timezone.utc))

    >>> middle.config.no_transit_local_dtime = True

    >>> TestModel(value=(2018, 7, 18, 14, 0))
    TestModel(value=datetime.datetime(2018, 7, 18, 14, 0, tzinfo=datetime.timezone.utc))

    >>> TestModel(value=datetime(2018, 7, 18, 14))
    TestModel(value=datetime.datetime(2018, 7, 18, 14, 0, tzinfo=datetime.timezone.utc))

    >>> TestModel(value="2018-07-18T14:00:00")
    TestModel(value=datetime.datetime(2018, 7, 18, 14, 0, tzinfo=datetime.timezone.utc))

If an input is not naive, it will be transformed to UTC regardless the value of ``no_transit_local_dtime``:

.. code-block:: pycon

    >>> from datetime import datetime, timezone
    >>> import middle

    >>> class TestModel(middle.Model):
    ...     value = middle.field(type=datetime)

    >>> # quick hack to get the local timezone
    ... current_tz = datetime.now(timezone.utc).astimezone().tzinfo

    >>> current_tz
    datetime.timezone(datetime.timedelta(-1, 75600), '-03')

    >>> middle.config.no_transit_local_dtime
    False

    >>> TestModel(value=datetime(2018, 7, 18, 14, 0, tzinfo=current_tz))
    TestModel(value=datetime.datetime(2018, 7, 18, 17, 0, tzinfo=datetime.timezone.utc))

    >>> TestModel(value=(2018, 7, 18, 14, 0, 0, 0, -3))
    TestModel(value=datetime.datetime(2018, 7, 18, 17, 0, tzinfo=datetime.timezone.utc))

    >>> TestModel(value="2018-07-18T14:00:00-03:00")
    TestModel(value=datetime.datetime(2018, 7, 18, 17, 0, tzinfo=datetime.timezone.utc))

    >>> middle.config.no_transit_local_dtime = True

    >>> TestModel(value=datetime(2018, 7, 18, 14, 0, tzinfo=current_tz))
    TestModel(value=datetime.datetime(2018, 7, 18, 17, 0, tzinfo=datetime.timezone.utc))

    >>> TestModel(value=(2018, 7, 18, 14, 0, 0, 0, -3))
    TestModel(value=datetime.datetime(2018, 7, 18, 17, 0, tzinfo=datetime.timezone.utc))

    >>> TestModel(value="2018-07-18T14:00:00-03:00")
    TestModel(value=datetime.datetime(2018, 7, 18, 17, 0, tzinfo=datetime.timezone.utc))

Temporary options
-----------------

``middle.config`` offers a context manager, called ``temp``, to provide all options as keywords inside the context for convenience:

.. code-block:: pycon

    >>> from datetime import datetime
    >>> import middle

    >>> class TestModel(middle.Model):
    ...     value = middle.field(type=datetime)

    >>> TestModel(value=(2018, 7, 18, 14, 0))
    TestModel(value=datetime.datetime(2018, 7, 18, 17, 0, tzinfo=datetime.timezone.utc))

    >>> with middle.config.temp(no_transit_local_dtime=True):
    ...     TestModel(value=(2018, 7, 18, 14, 0))

    TestModel(value=datetime.datetime(2018, 7, 18, 14, 0, tzinfo=datetime.timezone.utc))

    >>> middle.config.no_transit_local_dtime
    False

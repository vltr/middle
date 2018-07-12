.. _usage:

================
Using ``middle``
================

After installing ``middle``, it is easy to use it in your project. Most of its functionalities are acessible within the ``middle`` module already:

.. code-block:: python

    import middle

``middle`` consists basically in three parts:

- ``middle.Model``: the base class that needs to be inherited to declare all your models (except submodels);
- ``middle.field``: a function that is used to declare your field models; and
- ``middle.asdict``: a function required to convert your model instances to Python primitives.

``middle.Model``
----------------

The ``middle.Model`` class is the heart of ``middle``. To have all middle functionality at your disposal, ``middle.Model`` needs to be subclassed when declaring your models:

.. code-block:: python

    class MyModel(middle.Model):
        name: str = middle.field()  # Python 3.6+ syntax
        name = middle.field(type=str)  # Python 3.5 syntax

In essence, ``middle.Model`` started as a syntactic sugar for the ``attr.s`` decorator but soon evolved to a more complex design, implementing its own ``metaclass`` to handle some aspects of its models and fields.

.. note::

    Since ``middle.Model`` already implements its own ``metaclass``, it should be wise not to mix it with other classes that have a ``metaclass`` different than ``type``.

To create an instance of your model, you can:

- Use keyword arguments:

    .. code-block:: pycon

        >>> MyModel(name="foo")
        MyModel(name='foo')

- Use a ``dict``:

    .. code-block:: pycon

        >>> MyModel({"name": "foo"})
        MyModel(name='foo')

- Use a ``dict`` as ``**kwargs``:

    .. code-block:: pycon

        >>> MyModel(**{"name": "foo"})
        MyModel(name='foo')

- Use any ``object`` instance that have acessible attributes with the same name as the required ones from your model:

    .. code-block:: pycon

        >>> MyModel(some_obj_with_name_accessible)
        MyModel(name='foo')

``middle.field``
----------------

The ``middle.field`` function is used to declare your model's fields, with support to the type definition and other options that can be used later to define your model behavior regarding converting input values, :ref:`validating <validating>` values and format values for Python primitives. ``middle.field`` makes heavy usage of ``attr.ib`` calls, specially to store information into the ``metadata`` dict.

There are three ways to declare your fields inside ``middle.Model``, you don't have to necessarily use ``middle.field``, though it will be called under the hood to have a uniform model.

Declaring models, using ``middle.field`` and ``typing`` hints and annotations (`PEP-526 <https://www.python.org/dev/peps/pep-0526/>`_, for Python 3.6+):

.. code-block:: python

    class MyModel(middle.Model):
        id: int = middle.field()
        name: str = middle.field(min_length=5)
        active: bool = middle.field(default=False)
        created_on: datetime = middle.field(default=None)

Declaring models, using ``middle.field`` and ``type`` keyword (Python 3.5 compatible):

.. code-block:: python

    class MyModel(middle.Model):
        id = middle.field(type=int)
        name = middle.field(type=str, min_length=5)
        active = middle.field(type=bool, default=False)
        created_on = middle.field(type=datetime, default=None)

Declaring models, without ``middle.field``, using ``typing`` hints, annotations (Python 3.6+ only) and a ``dict``:

.. code-block:: python

    class MyModel(middle.Model):
        # id: int  # or ...
        id: int = {}
        name: str = {"min_length": 5}
        active: bool = {"default": False}
        created_on: datetime = {"default": None}

Declaring models, without ``middle.field``, using only a ``dict`` (Python 3.5 compatible):

.. code-block:: python

    class MyModel(middle.Model):
        id = {"type": int}
        name = {"type": str, "min_length": 5}
        active = {"type": str, "default": False}
        created_on = {"type": datetime, "default": None}

Declaring models, without ``middle.field``, using only ``typing`` hints and annotations (inspired by `pydantic <https://pydantic-docs.helpmanual.io/>`_, works only with Python 3.6+):

.. code-block:: python

    class MyModel(middle.Model):
        id: int
        name: str
        active: str
        created_on: datetime

.. warning::

    Declaring models using only ``typing`` hints annotations will not enable support for keyword embed :ref:`validators <validating>`.

Declaring models, the chaotic way (won't work on Python 3.5):

.. code-block:: python

    class MyModel(middle.Model):
        id: int
        name = {"type": str, "min_length": 5}
        active: bool = middle.field(default=False)
        created_on = middle.field(type=datetime, default=None)

.. tip::

    Developers are free to choose their preferred style (matching the Python version), although sticking to one can help readabilty.

``middle.asdict``
-----------------

This method, provided with an instance of a ``middle.Model`` class, will return a ``dict`` of key-values that will reflect the data of the instance against the model ``typing`` hints **only**.

.. code-block:: pycon

    >>> instance = MyModel(
    ...     id=42,
    ...     name="foo bar",
    ...     created_on=datetime.utcnow()
    ... )

    >>> instance
    MyModel(id=42, name='foo bar', active=False, created_on=datetime.datetime(2018, 7, 5, 14, 14, 12, 319270))

    >>> middle.asdict(instance)
    {'id': 42, 'name': 'foo bar', 'active': False, 'created_on': '2018-07-05T17:14:12.319270+00:00'}

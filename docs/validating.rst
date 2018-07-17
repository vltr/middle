.. _validating:

===============
Validating data
===============

Some types on ``middle`` can be validated based on single or multiple keywords that can be available to the ``field`` method, but will only trigger validation based on the type of the ``field``.

.. tip::

    Validation on ``middle`` is based on rules declared in the `OpenAPI specification <https://swagger.io/docs/specification/data-models/data-types/>`_, so most of them should not be strange to those familiar with web development.

.. important::

    All types have at least one validator: asserting if the type of the value is the one defined in the class (or None, if ``typing.Optional`` or have the keyword ``default`` set to ``None``).

.. warning::

    All validators that corresponds to a certain type will be called. This behavior may change in the future because I simply don't know if, in the OpenAPI specification, one (certain validator) may exclude another.

Range validators
----------------

There are some validators that works within a certain range that may contains a ``max`` and a ``min`` value (with keywords specific for a type). Given these values are *mostly quantitatives*, they cannot be negative (or ``ValueError`` will be raised), except for instances of type ``int`` or ``float``; nor the upper bound value can be equal or less than the lower bound value. Some other keywords may have some effect on these values as well.

.. math::
    lower\_bound \lt value \lt upper\_bound

.. important::

    Optionally range validators can also be used only with the ``lower_bound`` or ``upper_bound`` value if no bound is needed in one of the values.

String validators
-----------------

There are some validators for the ``str`` type that can

Range: ``min_length`` and ``max_length``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. math::
    min\_length \leqslant len(value) \leqslant max\_length

Setting ``min_length`` keyword to an integer would require that the input value should have at least the given value of length:

.. code-block:: pycon

    >>> import middle

    >>> class TestModel(middle.Model):
    ...     name = middle.field(type=str, min_length=3)

    >>> TestModel(name="hello")
    TestModel(name='hello')

    >>> TestModel(name="hi")

Given the input value above, here's the resulting ``Traceback``:

.. code-block:: pytb

    Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
    File "/home/dev/middle/src/middle/model.py", line 80, in __call__
        return super().__call__(**kwargs)
    File "<attrs generated init 70f3aaa3ccac019c22d47311619cd3804d1a9311>", line 4, in __init__
    File "/home/dev/.pyenv/versions/middle-3.6.6/lib/python3.6/site-packages/attr/_make.py", line 1668, in __call__
        v(inst, attr, value)
    File "/home/dev/middle/src/middle/validators/common.py", line 11, in wrapper
        return func(meta_value, instance, attribute, value)
    File "/home/dev/middle/src/middle/validators/common.py", line 21, in min_str_len
        attribute.name, meta_value
    middle.exceptions.ValidationError: 'name' must have a minimum length of 3 chars

Setting the ``max_length`` keyword to an integer would require that the input value should have no more than the given value of length:

.. code-block:: pycon

    >>> import middle

    >>> class TestModel(middle.Model):
    ...     name: str = middle.field(max_length=5)

    >>> TestModel(name="hello")
    TestModel(name='hello')

    >>> TestModel(name="hello, world")

.. code-block:: pytb

    Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
    File "/home/dev/middle/src/middle/model.py", line 80, in __call__
        return super().__call__(**kwargs)
    File "<attrs generated init 9b3b7c0ce74ad8f645d202b99d5df010c034e2b0>", line 4, in __init__
    File "/home/dev/.pyenv/versions/middle-3.6.6/lib/python3.6/site-packages/attr/_make.py", line 1668, in __call__
        v(inst, attr, value)
    File "/home/dev/middle/src/middle/validators/common.py", line 11, in wrapper
        return func(meta_value, instance, attribute, value)
    File "/home/dev/middle/src/middle/validators/common.py", line 31, in max_str_len
        attribute.name, meta_value
    middle.exceptions.ValidationError: 'name' must have a maximum length of 5 chars

``pattern``
~~~~~~~~~~~

Setting the ``pattern`` keyword to a string representing a regular expression (or a regular expression object) would require that the input value should match the value given:

.. code-block:: pycon

    >>> import middle

    >>> class TestModel(middle.Model):
    ...     serial = {"type": str, "pattern": "^[0-9]+$"}

    >>> TestModel(serial="123456")
    TestModel(serial='123456')

    >>> TestModel(serial="hello")

.. code-block:: pytb

    Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
    File "/home/dev/middle/src/middle/model.py", line 80, in __call__
        return super().__call__(**kwargs)
    File "<attrs generated init c36746f22b6ca0b15b44dff2665d92e7478d9031>", line 4, in __init__
    File "/home/dev/.pyenv/versions/middle-3.6.6/lib/python3.6/site-packages/attr/_make.py", line 1668, in __call__
        v(inst, attr, value)
    File "/home/dev/middle/src/middle/validators/common.py", line 11, in wrapper
        return func(meta_value, instance, attribute, value)
    File "/home/dev/middle/src/middle/validators/common.py", line 41, in str_pattern
        attribute.name, meta_value
    middle.exceptions.ValidationError: 'serial' did not match the given pattern: '^[0-9]+$'

``format``
~~~~~~~~~~

To be developed.

Number validators
-----------------

Range: ``minimum`` and ``maximum``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. math::
    minimum \leqslant value \leqslant maximum

Setting ``minimum`` keyword to an integer or float would require that the input value should have at least the required minimum value:

.. code-block:: pycon

    >>> import middle

    >>> class TestModel(middle.Model):
    ...     value = {"type": int, "minimum": 5}

    >>> TestModel(value=5)
    TestModel(value=5)

    >>> TestModel(value=20)
    TestModel(value=20)

    >>> TestModel(value=4)

.. code-block:: pytb

    Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
    File "/home/dev/middle/src/middle/model.py", line 105, in __call__
        return super().__call__(**kwargs)
    File "<attrs generated init 6ed99d543406ed37c7405962f27f473476610ca9>", line 4, in __init__
    File "/home/dev/.pyenv/versions/middle-3.6.6/lib/python3.6/site-packages/attr/_make.py", line 1668, in __call__
        v(inst, attr, value)
    File "/home/dev/middle/src/middle/validators/common.py", line 10, in wrapper
        return func(meta_value, instance, attribute, value)
    File "/home/dev/middle/src/middle/validators/common.py", line 60, in min_num_value
        attribute.name, meta_value
    middle.exceptions.ValidationError: 'value' must have a minimum value of 5

Setting the ``maximum`` keyword to an integer or float would require that the input value shoud have no more than the maximum value:

.. code-block:: pycon

    >>> import middle

    >>> class TestModel(middle.Model):
    ...     value: float = middle.field(maximum=3.14)

    >>> TestModel(value=-5.0)
    TestModel(value=-5.0)

    >>> TestModel(value=3.141)

.. code-block:: pytb

    Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
    File "/home/dev/middle/src/middle/model.py", line 105, in __call__
        return super().__call__(**kwargs)
    File "<attrs generated init 9fda1659ea481e0eb60414e362b3bd445d031dd3>", line 4, in __init__
    File "/home/dev/.pyenv/versions/middle-3.6.6/lib/python3.6/site-packages/attr/_make.py", line 1668, in __call__
        v(inst, attr, value)
    File "/home/dev/middle/src/middle/validators/common.py", line 10, in wrapper
        return func(meta_value, instance, attribute, value)
    File "/home/dev/middle/src/middle/validators/common.py", line 79, in max_num_value
        attribute.name, meta_value
    middle.exceptions.ValidationError: 'value' must have a maximum value of 3.14

``exclusive_minimum``
^^^^^^^^^^^^^^^^^^^^^

.. math::
    minimum \lt value

The ``exclusive_minimum`` keyword, being ``True``, would exclude the ``minimum`` value from the validation:

.. code-block:: pycon

    >>> import middle

    >>> class TestModel(middle.Model):
    ...     value = {"type": int, "minimum": 5, "exclusive_minimum": True}

    >>> TestModel(value=6)
    TestModel(value=6)

    >>> TestModel(value=5)

.. code-block:: pytb

    Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
    File "/home/dev/middle/src/middle/model.py", line 105, in __call__
        return super().__call__(**kwargs)
    File "<attrs generated init 29f97f0418f12486a7312929799ce2293fc24900>", line 4, in __init__
    File "/home/dev/.pyenv/versions/middle-3.6.6/lib/python3.6/site-packages/attr/_make.py", line 1668, in __call__
        v(inst, attr, value)
    File "/home/dev/middle/src/middle/validators/common.py", line 10, in wrapper
        return func(meta_value, instance, attribute, value)
    File "/home/dev/middle/src/middle/validators/common.py", line 53, in min_num_value
        attribute.name, meta_value
    middle.exceptions.ValidationError: 'value' must have a (exclusive) minimum value of 5

``exclusive_maximum``
^^^^^^^^^^^^^^^^^^^^^

.. math::
    value \lt maximum

The ``exclusive_maximum`` keyword, being ``True``, would exclude the ``maximum`` value from the validation:

.. code-block:: pycon

    >>> import middle

    >>> class TestModel(middle.Model):
    ...     value: float = middle.field(maximum=3.14, exclusive_maximum=True)

    >>> TestModel(value=3.1)
    TestModel(value=3.1)

    >>> TestModel(value=3.14)

.. code-block:: pytb

    Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
    File "/home/dev/middle/src/middle/model.py", line 105, in __call__
        return super().__call__(**kwargs)
    File "<attrs generated init 08e8fcc18b83475440f4c0239321aa61610c38b9>", line 4, in __init__
    File "/home/dev/.pyenv/versions/middle-3.6.6/lib/python3.6/site-packages/attr/_make.py", line 1668, in __call__
        v(inst, attr, value)
    File "/home/dev/middle/src/middle/validators/common.py", line 10, in wrapper
        return func(meta_value, instance, attribute, value)
    File "/home/dev/middle/src/middle/validators/common.py", line 72, in max_num_value
        attribute.name, meta_value
    middle.exceptions.ValidationError: 'value' must have a (exclusive) maximum value of 3.14

``multiple_of``
~~~~~~~~~~~~~~~

.. math::
    value {\rm\ mod\ }multiple\_of = 0

The ``multiple_of`` keyword specifies the multiple value that a value must have in order to have no remainder in a division operation. It works with ``int`` and ``float`` as well.

.. code-block:: pycon

    >>> import middle

    >>> class TestModel(middle.Model):
    ...     value = {"type": int, "multiple_of": 3}

    >>> TestModel(value=21)
    TestModel(value=21)

    >>> TestModel(value=22)

.. code-block:: pytb

    Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
    File "/home/dev/middle/src/middle/model.py", line 105, in __call__
        return super().__call__(**kwargs)
    File "<attrs generated init c24a18c0830f91f6079d00bbafff7e05f204e5a4>", line 4, in __init__
    File "/home/dev/.pyenv/versions/middle-3.6.6/lib/python3.6/site-packages/attr/_make.py", line 1668, in __call__
        v(inst, attr, value)
    File "/home/dev/middle/src/middle/validators/common.py", line 10, in wrapper
        return func(meta_value, instance, attribute, value)
    File "/home/dev/middle/src/middle/validators/common.py", line 96, in num_multiple_of
        "'{}' must be multiple of {}".format(attribute.name, meta_value)
    middle.exceptions.ValidationError: 'value' must be multiple of 3

List and Set validators
-----------------------

Range: ``min_items`` and ``max_items``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. math::
    min\_items \leqslant len(value) \leqslant max\_items

Setting ``min_items`` keyword to a List or Set would require that the input value should have at least the required number of items:

.. code-block:: pycon

    >>> import middle

    >>> class TestModel(middle.Model):
    ...     value = {"type": List[int], "min_items": 3}

    >>> TestModel(value=[1, 2, 3, 4])
    TestModel(value=[1, 2, 3, 4])

    >>> TestModel(value=[1, 2])

.. code-block:: pytb

    Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
    File "/home/dev/middle/src/middle/model.py", line 105, in __call__
        return super().__call__(**kwargs)
    File "<attrs generated init e1f1466567f03e1497438574116bf161e9400995>", line 4, in __init__
    File "/home/dev/.pyenv/versions/middle-3.6.6/lib/python3.6/site-packages/attr/_make.py", line 1668, in __call__
        v(inst, attr, value)
    File "/home/dev/middle/src/middle/validators/common.py", line 10, in wrapper
        return func(meta_value, instance, attribute, value)
    File "/home/dev/middle/src/middle/validators/common.py", line 104, in list_min_items
        "'{}' has no enough items of {}".format(attribute.name, meta_value)
    middle.exceptions.ValidationError: 'value' has no enough items of 3

Setting the ``max_items`` keyword to a List or Set would require that the input value shoud have no more than the required number of items:

.. code-block:: pycon

    >>> import middle

    >>> class TestModel(middle.Model):
    ...     value: List[int] = middle.field(max_items=5)

    >>> TestModel(value=[1, 2, 3, 4])
    TestModel(value=[1, 2, 3, 4])

    >>> TestModel(value=[1, 2, 3, 4, 5, 6])

.. code-block:: pytb

    Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
    File "/home/dev/middle/src/middle/model.py", line 105, in __call__
        return super().__call__(**kwargs)
    File "<attrs generated init 5180f70ad2fab18f88a0d4d0079cfcf36c2eb02a>", line 4, in __init__
    File "/home/dev/.pyenv/versions/middle-3.6.6/lib/python3.6/site-packages/attr/_make.py", line 1668, in __call__
        v(inst, attr, value)
    File "/home/dev/middle/src/middle/validators/common.py", line 10, in wrapper
        return func(meta_value, instance, attribute, value)
    File "/home/dev/middle/src/middle/validators/common.py", line 113, in list_max_items
        attribute.name, meta_value
    middle.exceptions.ValidationError: 'value' has more items than the limit of 5

``unique_items``
~~~~~~~~~~~~~~~~

The ``unique_items`` keyword specifies that all values in the input value should be unique.

.. code-block:: pycon

    >>> import middle

    >>> class TestModel(middle.Model):
    ...     value: List[int] = middle.field(unique_items=True)

    >>> TestModel(value=[1, 2, 3, 4])
    TestModel(value=[1, 2, 3, 4])

    >>> TestModel(value=[1, 2, 3, 2])

.. code-block:: pytb

    Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
    File "/home/dev/middle/src/middle/model.py", line 105, in __call__
        return super().__call__(**kwargs)
    File "<attrs generated init 1687613eb0214900b54beb0d1c7a7831de866678>", line 4, in __init__
    File "/home/dev/.pyenv/versions/middle-3.6.6/lib/python3.6/site-packages/attr/_make.py", line 1668, in __call__
        v(inst, attr, value)
    File "/home/dev/middle/src/middle/validators/common.py", line 10, in wrapper
        return func(meta_value, instance, attribute, value)
    File "/home/dev/middle/src/middle/validators/common.py", line 126, in list_unique_items
        "'{}' must only have unique items".format(attribute.name)
    middle.exceptions.ValidationError: 'value' must only have unique items

.. important::

    Remember that, to be unique, one value should be comparable with another. If you are comparing instances of models created with ``middle``, please take a look on :ref:`some tips <attrs>` regarding ``attrs``.

Dict validators
---------------

Range: ``min_properties`` and ``max_properties``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. math::
    min\_properties \leqslant len(value) \leqslant max\_properties

Setting ``min_properties`` keyword to a Dict would require that the input value should have at least the required number of keys and values:

.. code-block:: pycon

    >>> import middle

    >>> class TestModel(middle.Model):
    ...     value = {"type": Dict[str, int], "min_properties": 2}

    >>> TestModel(value={"hello": 1, "world": 2})
    TestModel(value={'hello': 1, 'world': 2})

    >>> TestModel(value={"foo": 99})

.. code-block:: pytb

    Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
    File "/home/dev/middle/src/middle/model.py", line 105, in __call__
        return super().__call__(**kwargs)
    File "<attrs generated init 95407a54d787ed82415f9e4fc5762a3d1642f501>", line 4, in __init__
    File "/home/dev/.pyenv/versions/middle-3.6.6/lib/python3.6/site-packages/attr/_make.py", line 1668, in __call__
        v(inst, attr, value)
    File "/home/dev/middle/src/middle/validators/common.py", line 10, in wrapper
        return func(meta_value, instance, attribute, value)
    File "/home/dev/middle/src/middle/validators/common.py", line 136, in dict_min_properties
        attribute.name, meta_value
    middle.exceptions.ValidationError: 'value' has no enough properties of 2

Setting the ``max_properties`` keyword to a Dict would require that the input value shoud have no more than the required number of keys and values:

.. code-block:: pycon

    >>> import middle

    >>> class TestModel(middle.Model):
    ...     value: Dict[str, int] = middle.field(max_properties=3)

    >>> TestModel(value={"hello": 1, "world": 2})
    TestModel(value={'hello': 1, 'world': 2})

    >>> TestModel(value={"hello": 1, "world": 2, "foo": 3, "bar": 4})

.. code-block:: pytb

    Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
    File "/home/dev/middle/src/middle/model.py", line 105, in __call__
        return super().__call__(**kwargs)
    File "<attrs generated init dc8195b57024445a6dc3a09749cde9f62b46333d>", line 4, in __init__
    File "/home/dev/.pyenv/versions/middle-3.6.6/lib/python3.6/site-packages/attr/_make.py", line 1668, in __call__
        v(inst, attr, value)
    File "/home/dev/middle/src/middle/validators/common.py", line 10, in wrapper
        return func(meta_value, instance, attribute, value)
    File "/home/dev/middle/src/middle/validators/common.py", line 147, in dict_max_properties
        attribute.name, meta_value
    middle.exceptions.ValidationError: 'value' has more properties than the limit of 3

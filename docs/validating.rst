.. _validating:

===============
Validating data
===============

Some types on ``middle`` can be validated based on single or multiple keywords that can be available to the ``field`` method, but will only trigger validation based on the type of the ``field``.

.. tip::

    Validation on ``middle`` is based on rules declared in the `OpenAPI specification <https://swagger.io/docs/specification/data-models/data-types/>`_, so most of them should not be strange to those familiar with web development.

Available validators
--------------------

``min_length``
~~~~~~~~~~~~~~

Only available for ``str``, it would require that the input value should have at least the given value of length:

.. code-block:: pycon

    >>> import middle

    >>> class TestModel(middle.Model):
    ...     name = middle.field(type=str, min_length=3)

    >>> TestModel(name="hello")
    TestModel(name='hello')

    >>> TestModel(name="hi")
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

``max_length``
~~~~~~~~~~~~~~

Only available for ``str``, it would require that the input value should have no more than the given value of length:

.. code-block:: pycon

    >>> import middle

    >>> class TestModel(middle.Model):
    ...     name: str = middle.field(max_length=5)

    >>> TestModel(name="hello")
    TestModel(name='hello')

    >>> TestModel(name="hello, world")
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

Only available for ``str``, it would require that the input value should match the Regex value given:

.. code-block:: pycon

    >>> import middle

    >>> class TestModel(middle.Model):
    ...     serial = {"type": str, "pattern": "^[0-9]+$"}

    >>> TestModel(serial="123456")
    TestModel(serial='123456')

    >>> TestModel(serial="hello")
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

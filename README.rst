========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis| |appveyor| |requires|
        | |codecov|
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|

.. |docs| image:: https://readthedocs.org/projects/middle/badge/?style=flat
    :target: https://readthedocs.org/projects/middle
    :alt: Documentation Status

.. |travis| image:: https://travis-ci.org/vltr/middle.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/vltr/middle

.. |appveyor| image:: https://ci.appveyor.com/api/projects/status/github/vltr/middle?branch=master&svg=true
    :alt: AppVeyor Build Status
    :target: https://ci.appveyor.com/project/vltr/middle

.. |requires| image:: https://requires.io/github/vltr/middle/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/vltr/middle/requirements/?branch=master

.. |codecov| image:: https://codecov.io/github/vltr/middle/coverage.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/vltr/middle

.. |version| image:: https://img.shields.io/pypi/v/middle.svg
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/middle

.. |commits-since| image:: https://img.shields.io/github/commits-since/vltr/middle/v0.1.0.svg
    :alt: Commits since latest release
    :target: https://github.com/vltr/middle/compare/v0.1.0...master

.. |wheel| image:: https://img.shields.io/pypi/wheel/middle.svg
    :alt: PyPI Wheel
    :target: https://pypi.python.org/pypi/middle

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/middle.svg
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/middle

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/middle.svg
    :alt: Supported implementations
    :target: https://pypi.python.org/pypi/middle

.. |codestyle| image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :alt: Code style: black
    :target: https://github.com/ambv/black

.. end-badges

Flexible, extensible Python data structures for general usage

* Free software: MIT license

Installation
============

::

    pip install middle

Documentation
=============

https://middle.readthedocs.io/

Development
===========

To run the all tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox

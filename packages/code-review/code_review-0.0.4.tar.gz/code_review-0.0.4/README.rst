========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis|
        | |codecov|
        | |landscape|
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|

.. |travis| image:: https://travis-ci.org/sagersmith8/code_review.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/sagersmith8/code_review

.. |codecov| image:: https://codecov.io/github/sagersmith8/code_review/coverage.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/sagersmith8/code_review

.. |landscape| image:: https://landscape.io/github/sagersmith8/code_review/master/landscape.svg?style=flat
    :target: https://landscape.io/github/sagersmith8/code_review/master
    :alt: Code Quality Status

.. |version| image:: https://img.shields.io/pypi/v/code_review.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/code_review

.. |commits-since| image:: https://img.shields.io/github/commits-since/sagersmith8/code_review/v0.0.1.svg
    :alt: Commits since latest release
    :target: https://github.com/sagersmith8/code_review/compare/v0.0.1...master

.. |wheel| image:: https://img.shields.io/pypi/wheel/code_review.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/code_review

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/code_review.svg
    :alt: Supported versions
    :target: https://pypi.org/project/code_review

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/code_review.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/code_review


.. end-badges

Creates links for PR updates

* Free software: Apache Software License 2.0

Installation
============

::

    pip install code_review

Documentation
=============


To use the project:

.. code-block:: bash

    $ python -m code_review -h
    usage: code_review [-h] [-o] [-s] [-t TOKEN]

    Command description.

    optional arguments:
      -h, --help            show this help message and exit
      -o, --open            Opens new code review updates in default browser
      -s, --stdout          Prints code review updates
      -t TOKEN, --token TOKEN
                        Token to use when checking for updates


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

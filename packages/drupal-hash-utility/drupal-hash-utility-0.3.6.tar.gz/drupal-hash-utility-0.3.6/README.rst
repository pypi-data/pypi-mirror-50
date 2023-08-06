========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - | `docs <https://gitlab.com/thaxoo/drupal_hash_utility/blob/master/README.rst>`_ v0.3.6.
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|

.. |version| image:: https://img.shields.io/pypi/v/drupal-hash-utility.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/drupal-hash-utility

.. |wheel| image:: https://img.shields.io/pypi/wheel/drupal-hash-utility.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/drupal-hash-utility

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/drupal-hash-utility.svg
    :alt: Supported versions
    :target: https://pypi.org/project/drupal-hash-utility

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/drupal-hash-utility.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/drupal-hash-utility


.. end-badges

A hashing utility built from Drupal7 specification.

* Free software: MIT license

Installation
============

::

    pip install drupal-hash-utility

Documentation
=============


To use the project:

.. code-block:: python

    import drupal_hash_utility


    drash = DrupalHashUtility()

    # Read the Help Docs
    print(help(drash))


    # Generate Drupal7 Hash
    password = 'P@ssw0rd'
    encoded = drash.encode(password)

    # Verify Password Against Hash
    drash.verify(password, encoded)

    # Get Hash Summary
    drash.summary(encoded)


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

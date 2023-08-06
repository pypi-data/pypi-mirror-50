
***********************************************
squint: Simple query interface for tabular data
***********************************************

..
    Project badges for quick reference:

|buildstatus| |devstatus| |license| |pyversions|


.. start-inclusion-marker-description

Datatest helps speed up and formalize data-wrangling and data
validation tasks. It repurposes software testing practices for
data preparation and quality assurance projects. Datatest can
help you:

* Clean and wrangle data faster and more accurately.
* Maintain a record of checks and decisions regarding important data sets.
* Distinguish between ideal criteria and acceptible deviation.
* Measure progress of data preparation tasks.
* On-board new team members with an explicit and structured process.
* Test data pipeline components and end-to-end behavior.

Datatest supports both pytest_ and unittest_ style testing.
It implements a system of validation methods, difference
classes, and acceptance context managers.

Datatest has no hard dependencies; supports Python 2.6, 2.7,
3.1 through 3.8, PyPy, and PyPy3; and is freely available under
the Apache License, version 2.

.. _pytest: https://pytest.org
.. _unittest: https://docs.python.org/library/unittest.html

.. end-inclusion-marker-description


:Documentation:
    | https://squint.readthedocs.io/ (stable)
    | https://squint.readthedocs.io/en/latest/ (latest)

:Official:
    | https://pypi.org/project/squint/


Installation
============

.. start-inclusion-marker-install

The easiest way to install squint is to use `pip <https://pip.pypa.io>`_::

  pip install squint

To upgrade an existing installation, use the "``--upgrade``" option::

  pip install --upgrade squint


Stuntman Mike
-------------

If you need bug-fixes or features that are not available
in the current stable release, you can "pip install" the
development version directly from GitHub::

  pip install --upgrade https://github.com/shawnbrown/datatest/archive/master.zip

All of the usual caveats for a development install should
apply---only use this version if you can risk some instability
or if you know exactly what you're doing. While care is taken
to never break the build, it can happen.


Safety-first Clyde
------------------

If you need to review and test packages before installing, you can
install datatest manually.

Download the latest **source** distribution from the Python Package
Index (PyPI):

  https://pypi.org/project/datatest/ (navigate to "Download files")

Unpack the file (replacing X.Y.Z with the appropriate version number)
and review the source code::

  tar xvfz datatest-X.Y.Z.tar.gz

Change to the unpacked directory and run the tests::

  cd datatest-X.Y.Z
  python setup.py test

Don't worry if some of the tests are skipped. Tests for optional data
sources (like pandas DataFrames or MS Excel files) are skipped when the
related third-party packages are not installed.

If the source code and test results are satisfactory, install the
package::

  python setup.py install

.. end-inclusion-marker-install


Supported Versions
==================

Tested on Python 2.6, 2.7, 3.2 through 3.8, PyPy, and PyPy3.
Datatest is pure Python and may also run on other implementations
as well (check using "setup.py test" before installing).


Development Repository
======================

The development repository for ``squint`` is hosted on
`GitHub <https://github.com/shawnbrown/squint>`_.


----------

Freely licensed under the Apache License, Version 2.0

Copyright 2014 - 2019 National Committee for an Effective Congress, et al.


..
  SUBSTITUTION DEFINITONS:

.. |buildstatus| image:: https://travis-ci.org/shawnbrown/squint.svg?branch=master
    :target: https://travis-ci.org/shawnbrown/squint
    :alt: Current Build Status

.. |devstatus| image:: https://img.shields.io/pypi/status/squint.svg
    :target: https://pypi.org/project/squint/
    :alt: Development Status

.. |license| image:: https://img.shields.io/badge/license-Apache%202-blue.svg
    :target: https://opensource.org/licenses/Apache-2.0
    :alt: Apache 2.0 License

.. |pyversions| image:: https://img.shields.io/pypi/pyversions/squint.svg
    :target: https://pypi.org/project/squint/#supported-versions
    :alt: Supported Python Versions

.. |githubstars| image:: https://img.shields.io/github/stars/shawnbrown/squint.svg
    :target: https://github.com/shawnbrown/squint/stargazers
    :alt: GitHub users who have starred this project

.. |pypiversion| image:: https://img.shields.io/pypi/v/squint.svg
    :target: https://pypi.org/project/squint/
    :alt: Current PyPI Version


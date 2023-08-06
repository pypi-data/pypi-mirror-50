panci
==========

.. image:: https://secure.travis-ci.org/msabramo/python-panci.png
   :target: http://travis-ci.org/msabramo/python-panci

For a Python project, take a ``.travis.yml`` file (`Travis CI`_) and output a
``tox.ini`` file (`Tox`_). Or vice-versa.

Why the name?
-------------

The name "panci" is an homage to `John MacFarlane`_'s excellent `pandoc`_.
I've replaced the "doc" with "ci"; "CI" stands for Continuous Integration, a broad term for what `Travis CI`_ and `Tox`_ help you with.

Installing
----------

With pip::

    pip install panci

Example
-------

Travis to Tox
~~~~~~~~~~~~~

Let's say that we have the following ``.travis.yml``:

.. code-block:: yaml

    language: python

    python:
      - 2.6
      - 2.7
      - 3.2
      - pypy

    script: python setup.py test

If we run::

    panci --to=tox .travis.yml

Then we get:

.. code-block:: ini

    # Tox (http://tox.testrun.org/) is a tool for running tests
    # in multiple virtualenvs. This configuration file will run the
    # test suite on all supported python versions. To use it, "pip install tox"
    # and then run "tox" from this directory.

    [tox]
    envlist = py26, py27, py32, pypy

    [testenv]
    commands = python setup.py test

Tox to Travis
~~~~~~~~~~~~~

Let's say that we have the following ``tox.ini``:

.. code-block:: ini

   [tox]
   envlist = py26, py27, py33, pypy

   [testenv]
   commands = py.test
   deps = pytest

If we run::

	panci tox.ini

Then we get:

.. code-block:: yaml

   language: python
   env:
     - TOXENV=py26
     - TOXENV=py27
     - TOXENV=py33
     - TOXENV=pypy
   install:
     - travis_retry pip install tox==1.6.1
   script:
     - travis_retry tox


panci-tox-quickstart
~~~~~~~~~~~~~~~~~~~~

If we run::

    panci-tox-quickstart

Then you are asked some questions::

    This utility will ask you a few questions and then generate a simple tox.ini
    file to help get you started using tox.

    Please enter values for the following settings (just press Enter to
    accept a default value, if one is given in brackets).

    > Test your project with py24 (Y/n) [Y]: n
    > Test your project with py25 (Y/n) [Y]: n
    > Test your project with py26 (Y/n) [Y]:
    > Test your project with py27 (Y/n) [Y]:
    > Test your project with py30 (Y/n) [Y]:
    > Test your project with py31 (Y/n) [Y]:
    > Test your project with py32 (Y/n) [Y]:
    > Test your project with py33 (Y/n) [Y]:
    > Test your project with pypy (Y/n) [Y]:
    > Test your project with jython (Y/n) [Y]: n

    What command should be used to test your project -- examples:
        - python setup.py test
        - nosetests package.module
        - trial package.module
    > Command to run to test project [{envpython} setup.py test]:

    What dependencies does your project have?
    > Comma-separated list of dependencies [ ]: requests,nose

    Creating file tox.ini.

    Finished: A tox.ini file has been created.

    Execute `tox` to test your project.

And then a ``tox.ini`` file is spit out with:

.. code-block:: ini

    # Tox (http://tox.testrun.org/) is a tool for running tests
    # in multiple virtualenvs. This configuration file will run the
    # test suite on all supported python versions. To use it, "pip install tox"
    # and then run "tox" from this directory.

    [tox]
    envlist = py26, py27, py30, py31, py32, py33, pypy

    [testenv]
    commands = {envpython} setup.py test
    deps =
        requests
        nose

Note about ``panci-tox-quickstart``: I am also working longer-term on getting a
``tox-quickstart`` command merged into tox. See `this pull request
<https://bitbucket.org/hpk42/tox/pull-request/20/add-a-tox-quickstart-command/diff>`_.


Miscellaneous related stuff
~~~~~~~~~~~~~~~~~~~~~~~~~~~

* `buildbot_travis`_ -- allows `Buildbot`_ to consume a ``.travis.yml`` file.


Support
~~~~~~~

For questions, comments, and suggestions, please use `GitHub Issues`_.

.. _John MacFarlane: http://johnmacfarlane.net/
.. _pandoc: http://johnmacfarlane.net/pandoc/
.. _Travis CI: http://travis-ci.org/
.. _Tox: http://tox.testrun.org/
.. _GitHub Issues: https://github.com/msabramo/python-panci/issues
.. _buildbot_travis: https://github.com/Jc2k/buildbot_travis
.. _Buildbot: http://buildbot.net/

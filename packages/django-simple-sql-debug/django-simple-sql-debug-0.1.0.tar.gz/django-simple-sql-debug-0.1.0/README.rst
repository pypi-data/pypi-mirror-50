=============================
sql_debug
=============================

.. image:: https://badge.fury.io/py/django-simple-sql-debug.svg
    :target: https://badge.fury.io/py/django-simple-sql-debug

.. image:: https://travis-ci.org/pylame22/django-simple-sql-debug.svg?branch=master
    :target: https://travis-ci.org/pylame22/django-simple-sql-debug

.. image:: https://codecov.io/gh/pylame22/django-simple-sql-debug/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/pylame22/django-simple-sql-debug

Your project description goes here

Documentation
-------------

The full documentation is at https://django-simple-sql-debug.readthedocs.io.

Quickstart
----------

Install sql_debug::

    pip install django-simple-sql-debug

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'sql_debug.apps.SqlDebugConfig',
        ...
    )

Add sql_debug's URL patterns:

.. code-block:: python

    from sql_debug import urls as sql_debug_urls


    urlpatterns = [
        ...
        url(r'^', include(sql_debug_urls)),
        ...
    ]

Features
--------

* TODO

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox

Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage

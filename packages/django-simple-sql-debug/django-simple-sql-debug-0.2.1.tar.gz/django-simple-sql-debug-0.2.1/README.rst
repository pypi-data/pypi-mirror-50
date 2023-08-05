=============================
sql_debug
=============================

.. image:: https://badge.fury.io/py/django-simple-sql-debug.svg
    :target: https://badge.fury.io/py/django-simple-sql-debug

.. image:: https://travis-ci.org/pylame22/django-simple-sql-debug.svg?branch=master
    :target: https://travis-ci.org/pylame22/django-simple-sql-debug

.. image:: https://codecov.io/gh/pylame22/django-simple-sql-debug/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/pylame22/django-simple-sql-debug

This application shows the database queries

Installation
-------------

Install sql_debug::

    pip install django-simple-sql-debug

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = [
        ...
        'sql_debug',
        ...
    ]

Add sql_debug's URL patterns:

.. code-block:: python

    from sql_debug import urls as sql_debug_urls


    urlpatterns = [
        ...
        path('sql_debug/', include(sql_debug_urls)),
        ...
    ]


Run migrate::

    python manage.py migrate

Settings
--------

.. code-block:: python

    SQL_DEBUG_PATHS_BLACKLIST = [
        '/sql_debug',
        '/admin',
        '/favicon.ico',
    ]  # by default

    SQL_DEBUG_MAX_REQUESTS = 20  # by default

------------

SQL_DEBUG_BLACKLISTED_PATHS
  A list of paths that are skipped by the application.

SQL_DEBUG_MAX_REQUESTS
  Maximum number of queries stored in the database.

Production
----------
Add in production_settings.py

.. code-block:: python

    # Remove django-sql-debug
    INSTALLED_APPS.remove('sql_debug')
    MIDDLEWARE.remove('sql_debug.middleware.SqlDebugMiddleware')


Add in urls.py

.. code-block:: python

    if settings.ENV == 'local':  # or (not settings.DEBUG)
        urlpatterns += [
            path('sql_debug/', include(sql_debug_urls)),
        ]

Screenshots
-----------

.. image:: demo-list.png
  :width: 800

.. image:: demo-detail.png
  :width: 800

Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage

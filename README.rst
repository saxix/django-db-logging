==================
Django DB Logging
==================

.. image:: https://badge.fury.io/py/django-db-logging.png
    :target: http://badge.fury.io/py/django-db-logging

.. image:: https://api.travis-ci.com/saxix/django-db-logging.png?branch=master
        :target: https://travis-ci.org/saxix/django-db-logging

.. image:: https://pypip.in/d/django-db-logging/badge.png
        :target: https://pypi.python.org/pypi/django-db-logging


Database logging handler with Django integration


This package contains two handlers fully compatible with python logging sub-system.
They allow to use standard logging functionalities and display log using Django Admin
interface.

This package is not intented to be used in production for high traffic web sites, it,
instead, has been developed to help a rapid troubleshooting in following scenarions:

    - User Acceptant Test environment

    - Small/Medium traffic application

    - Cloud environments where developer do not have access to logs

It contains two handlers:

    - `DBHandler`: synchronous logging to database

    - `AsyncDBHandler`: asynchronous logging to database. It helps to reduce the 'per request' user response time


Installation
------------

::

    pip install django-db-logging


Update your settings::


    INSTALLED_APPS = [
        ...
        'admin_extra_urls',
        'django_db_logging',
        ]

    LOGGING = {
        ...
        'handlers': {
            'db': {
                'level': 'DEBUG',
                'class': 'django_db_logging.handlers.AsyncDBHandler',
            },

        },
        'loggers': {
            '': {
                'handlers': ['db', 'console'],
                'level': 'ERROR'
            },
            'django_db_logging': {
                'handlers': ['console'],  # do not use 'db' here
                'propagate': False,  # do not propagate
                'level': 'ERROR'
            },
        }
    }

    DBLOG = {
        "MAX_LOG_ENTRIES" : 10000,  # max entries to keep
        "ENABLE_TEST_BUTTON": True, # Display 'Test' button in admin
        "ALLOW_TRUNCATE": True,     # Display 'Empty Log' button
        "USE_CRASHLOG":  False,     # enable django-crashlog integration
    }

It now possible use standard logging functionalities and see check logs in the Admin site.



**Note** It's better do not use this as unique handler, database connection can fails
and you could loose your log. Always add extra handler.


django-crashlog integration
~~~~~~~~~~~~~~~~~~~~~~~~~~~

DBLogger can be integrated with [django-crashlog](https://github.com/saxix/django-crashlog)
everytime an exception in logged (using `logger.exception`) an entry in `django-crashlog`
is automatically created without the needs to use `process_exception`


Logs cleanup
~~~~~~~~~~~~

If you use [celery]() or any other task runner you can schedule a daily cleanup
running `django_db_logging.models.Record.objects.cleanup` to delete all but `config.MAX_LOG_ENTRIES`
most recent lines


Use custom models
~~~~~~~~~~~~~~~~~

It is possible to customize handlers to use dedicated Model::

    from django_db_logging.models import AbstractRecord


    class CustomLogger(AbstractRecord):
        class Meta:
            app_label = 'demo'

and in your settings::

    LOGGING = {
        ...
        'handlers': {
            'db': {
                'level': 'DEBUG',
                'class': 'django_db_logging.handlers.AsyncDBHandler',
                'model': 'demo.CustomLogger',
            },

        },
        ...





Links
~~~~~

+--------------------+----------------+--------------+------------------------+
| Stable             | |master-build| | |master-cov| |                        |
+--------------------+----------------+--------------+------------------------+
| Development        | |dev-build|    | |dev-cov|    |                        |
+--------------------+----------------+--------------+------------------------+
| Project home page: | https://github.com/saxix/django-db-logging             |
+--------------------+---------------+----------------------------------------+
| Issue tracker:     | https://github.com/saxix/django-db-logging/issues?sort |
+--------------------+---------------+----------------------------------------+
| Download:          | http://pypi.python.org/pypi/django-db-logging/         |
+--------------------+---------------+----------------------------------------+
| Documentation:     | https://django-db-logging.readthedocs.org/en/latest/   |
+--------------------+---------------+--------------+-------------------------+

.. |master-build| image:: https://api.travis-ci.com/saxix/django-db-logging.png?branch=master
                    :target: http://travis-ci.com/saxix/django-db-logging/

.. |master-cov| image:: https://codecov.io/gh/saxix/django-db-logging/branch/master/graph/badge.svg
                    :target: https://codecov.io/gh/saxix/django-db-logging

.. |dev-build| image:: https://api.travis-ci.com/saxix/django-db-logger.png?branch=develop
                  :target: http://travis-ci.com/saxix/django-db-logging/

.. |dev-cov| image:: https://codecov.io/gh/saxix/django-db-logger/branch/develop/graph/badge.svg
                    :target: https://codecov.io/gh/saxix/django-db-logging




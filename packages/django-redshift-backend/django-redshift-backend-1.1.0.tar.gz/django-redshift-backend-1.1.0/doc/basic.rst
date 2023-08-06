=====
Basic
=====

Installation
============

Please install django-redshift-backend with using pip (8.1.1 or later).

.. code-block:: bash

   $ pip install django-redshift-backend


Django settings
===============

ENGINE for DATABASES is 'django_redshift_backend'. You can set the name in your settings.py as::

   DATABASES = {
       'default': {
           'ENGINE': 'django_redshift_backend',
           'NAME': '<your database name>',
           'USER': '<your database username>',
           'PASSWORD': '<your database password>',
           'HOST': '<your database hostname>',
           'PORT': '5439',
       }
   }

For more information, please refer :doc:`refs`.



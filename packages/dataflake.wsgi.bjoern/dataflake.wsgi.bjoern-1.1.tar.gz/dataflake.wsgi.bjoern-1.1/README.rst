.. image:: https://travis-ci.com/dataflake/dataflake.wsgi.bjoern.svg?branch=master
   :target: https://travis-ci.com/dataflake/dataflake.wsgi.bjoern

.. image:: https://coveralls.io/repos/github/dataflake/dataflake.wsgi.bjoern/badge.svg?branch=master
   :target: https://coveralls.io/github/dataflake/dataflake.wsgi.bjoern?branch=master

.. image:: https://readthedocs.org/projects/dataflakewsgibjoern/badge/?version=latest
   :target: https://dataflakewsgibjoern.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

.. image:: https://img.shields.io/pypi/v/dataflake.wsgi.bjoern.svg
   :target: https://pypi.org/project/dataflake.wsgi.bjoern/
   :alt: Current version on PyPI

.. image:: https://img.shields.io/pypi/pyversions/dataflake.wsgi.bjoern.svg
   :target: https://pypi.org/project/dataflake.wsgi.bjoern/
   :alt: Supported Python versions


dataflake.wsgi.bjoern
=====================

This package provides a PasteDeploy-compatible entry point to easily integrate
the `bjoern WSGI server <https://github.com/jonashaag/bjoern>`_ into an
environment that uses PasteDeploy-style ``.ini`` files to compose a WSGI
application.

It also includes a script to create a basic WSGI configuration file for Zope,
similar to Zope's own ``mkwsgiinstance``, but specifying ``bjoern`` instead of
``waitress`` as WSGI server.

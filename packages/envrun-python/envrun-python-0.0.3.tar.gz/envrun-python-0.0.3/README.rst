envrun-python
=============

.. image:: https://img.shields.io/pypi/v/envrun-python.svg
    :target: https://pypi.python.org/pypi/envrun-python
    :alt: Latest PyPI version

.. image:: https://travis-ci.org/ericgj/envrun-python.png
   :target: https://travis-ci.org/ericgj/envrun-python
   :alt: Latest Travis CI build status

Run command with specified environment-variable file

Install
-------

::

  pip install envrun-python


Usage
-----

Run specifying environment variables in YAML format::

  envrun -f env.yaml somecmd arg1 arg2


Or JSON, or .env format::

  envrun -f .env somecmd arg1 arg2


Run within a python virtualenv::

  envrun -e .venv pytest


That's basically it.

Note the .env format parser is taken from
`python-dotenv <https://github.com/theskumar/python-dotenv>`_.


Contact
-------

`Eric Gjertsen <ericgj72@gmail.com>`_.


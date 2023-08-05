Moose Frank
===========

A Python package packed with tools that are commonly used in Moose projects.


Installation
++++++++++++

.. code-block:: sh

    pip install moose-frank


Local testing
-------------

isort

.. code-block:: console

    docker-compose run --rm --no-deps python isort [module/path] [options]

-------------

flake8

.. code-block:: console

    docker-compose run --rm --no-deps python flake8 [module/path]

-------------

black

.. code-block:: console

    docker-compose run --rm --no-deps python black [module/path]

-------------

pytest

.. code-block:: console

    docker-compose run --rm --no-deps python coverage run ./runtests.py

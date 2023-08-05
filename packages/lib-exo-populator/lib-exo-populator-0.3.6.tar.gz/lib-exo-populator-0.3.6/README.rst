=============================
lib-exo-populator
=============================

.. image:: https://badge.fury.io/py/lib-exo-populator.svg
    :target: https://badge.fury.io/py/lib-exo-populator

.. image:: https://requires.io/github/exolever/lib-exo-populator/requirements.svg?branch=master
     :target: https://requires.io/github/exolever/lib-exo-populator/requirements/?branch=master
     :alt: Requirements Status

.. image:: https://travis-ci.org/exolever/lib-exo-populator.svg?branch=master
    :target: https://travis-ci.org/exolever/lib-exo-populator

.. image:: https://codecov.io/gh/exolever/lib-exo-populator/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/exolever/lib-exo-populator

.. image:: https://sonarcloud.io/api/project_badges/measure?project=exolever_lib-exo-populator&metric=alert_status
   :target: https://sonarcloud.io/dashboard?id=exolever_lib-exo-populator
   
.. image:: https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat
   :target: https://github.com/exolever/lib-exo-populator/issues
   
.. image:: https://img.shields.io/badge/License-MIT-green.svg
   :target: https://opensource.org/licenses/MIT

Generic populate models in django from YAML files


Quickstart
----------

Install exo_populator::

    pip install lib-exo-populator

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'populate',
        ...
    )

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

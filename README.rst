.. image:: http://www.repostatus.org/badges/latest/wip.svg
    :target: http://www.repostatus.org/#wip
    :alt: Project Status: WIP — Initial development is in progress, but there
          has not yet been a stable, usable release suitable for the public.

.. image:: https://github.com/jwodder/click-loglevel/workflows/Test/badge.svg?branch=master
    :target: https://github.com/jwodder/click-loglevel/actions?workflow=Test
    :alt: CI Status

.. image:: https://codecov.io/gh/jwodder/click-loglevel/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/jwodder/click-loglevel

.. image:: https://img.shields.io/github/license/jwodder/click-loglevel.svg
    :target: https://opensource.org/licenses/MIT
    :alt: MIT License

`GitHub <https://github.com/jwodder/click-loglevel>`_
| `Issues <https://github.com/jwodder/click-loglevel/issues>`_

``click-loglevel`` provides a ``LogLevelType`` parameter type for use in Click_
programs that wish to let the user set the logging level.  It accepts all of
the ``logging`` log level names (``CRITICAL``, ``ERROR``, ``WARNING``,
``INFO``, ``DEBUG``, and ``NOTSET``, all case insensitive), and converts them
into their corresponding numeric values.  It also accepts integer values and
leaves them as-is.

.. _Click: https://palletsprojects.com/p/click/


Installation
============
``click-loglevel`` requires Python 3.6 or higher.  Just use `pip
<https://pip.pypa.io>`_ for Python 3 (You have pip, right?) to install
``click-loglevel`` and its dependencies::

    python3 -m pip install click-loglevel


Example
========

``myscript.py``:

.. code:: python

    import logging
    import click
    from click_loglevel import LogLevelType

    @click.command()
    @click.option("-l", "--log-level", type=LogLevelType(), default=logging.INFO)
    def main(log_level):
        logging.basicConfig(
            format="%(asctime)s [%(levelname)-8s] %(name)s %(message)s",
            datefmt="%Y-%m-%dT%H:%M:%S%z",
            level=log_level,
        )
        ...

Running ``myscript.py``:

.. code:: console

    $ python3 myscript.py --log-level DEBUG
    # Log level is set to "DEBUG"
    $ python3 myscript.py --log-level error
    # Log level is set to "ERROR"
    $ python3 myscript.py --log-level 15
    # Log level is between DEBUG and INFO
.. image:: http://www.repostatus.org/badges/latest/active.svg
    :target: http://www.repostatus.org/#active
    :alt: Project Status: Active — The project has reached a stable, usable
          state and is being actively developed.

.. image:: https://github.com/jwodder/click-loglevel/workflows/Test/badge.svg?branch=master
    :target: https://github.com/jwodder/click-loglevel/actions?workflow=Test
    :alt: CI Status

.. image:: https://codecov.io/gh/jwodder/click-loglevel/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/jwodder/click-loglevel

.. image:: https://img.shields.io/pypi/pyversions/click-loglevel.svg
    :target: https://pypi.org/project/click-loglevel/

.. image:: https://img.shields.io/github/license/jwodder/click-loglevel.svg
    :target: https://opensource.org/licenses/MIT
    :alt: MIT License

`GitHub <https://github.com/jwodder/click-loglevel>`_
| `PyPI <https://pypi.org/project/click-loglevel/>`_
| `Issues <https://github.com/jwodder/click-loglevel/issues>`_
| `Changelog <https://github.com/jwodder/click-loglevel/blob/master/CHANGELOG.md>`_

``click-loglevel`` provides a ``LogLevel`` parameter type for use in Click_
programs that wish to let the user set the logging level.  It accepts all of
the ``logging`` log level names (``CRITICAL``, ``ERROR``, ``WARNING``,
``INFO``, ``DEBUG``, and ``NOTSET``, all case insensitive), and converts them
into their corresponding numeric values.  It also accepts integer values and
leaves them as-is.  Custom log levels are also supported.

.. _Click: https://palletsprojects.com/p/click/


Installation
============
``click-loglevel`` requires Python 3.6 or higher.  Just use `pip
<https://pip.pypa.io>`_ for Python 3 (You have pip, right?) to install
``click-loglevel`` and its dependencies::

    python3 -m pip install click-loglevel


Examples
========

``myscript.py``:

.. code:: python

    import logging
    import click
    from click_loglevel import LogLevel

    @click.command()
    @click.option("-l", "--log-level", type=LogLevel(), default=logging.INFO)
    def main(log_level):
        logging.basicConfig(
            format="[%(levelname)-8s] %(message)s",
            level=log_level,
        )
        logging.log(log_level, "Log level set to %r", log_level)

    if __name__ == "__main__":
        main()

Running ``myscript.py``:

.. code:: console

    $ python3 myscript.py --log-level DEBUG
    [DEBUG   ] Log level set to 10
    $ python3 myscript.py --log-level error
    [ERROR   ] Log level set to 40
    $ python3 myscript.py --log-level 15
    [Level 15] Log level set to 15

Script with custom log levels:

.. code:: python

    import logging
    import click
    from click_loglevel import LogLevel

    logging.addLevelName(15, "VERBOSE")
    logging.addLevelName(25, "NOTICE")

    @click.command()
    @click.option(
        "-l", "--log-level",
        type=LogLevel(extra=["VERBOSE", "NOTICE"]),
        default=logging.INFO,
    )
    def main(log_level):
        logging.basicConfig(
            format="[%(levelname)-8s] %(message)s",
            level=log_level,
        )
        logging.log(log_level, "Log level set to %r", log_level)

    if __name__ == "__main__":
        main()


API
===

The ``click_loglevel`` module contains a single class:

``LogLevel``
------------

A subclass of ``click.ParamType`` that accepts the standard logging level names
(case insensitive) and converts them to their corresponding numeric values.  It
also accepts integer values and leaves them as-is.

Custom log levels can be added by passing them as the ``extra`` argument to the
constructor.  ``extra`` can be either an iterable of level names (in which case
the levels must have already been defined — typically at the module level — by
calling ``logging.addLevelName()``) or a mapping from level names to their
corresponding values.  All custom log levels will be recognized case
insensitively; if two different level names differ only in case, the result is
undefined.

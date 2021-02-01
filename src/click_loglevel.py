"""
Log level parameter type for Click

``click-loglevel`` provides a ``LogLevelType`` parameter type for use in Click_
programs that wish to let the user set the logging level.  It accepts all of
the ``logging`` log level names (``CRITICAL``, ``ERROR``, ``WARNING``,
``INFO``, ``DEBUG``, and ``NOTSET``, all case insensitive), and converts them
into their corresponding numeric values.  It also accepts integer values and
leaves them as-is.

.. _Click: https://palletsprojects.com/p/click/

Visit <https://github.com/jwodder/click-loglevel> for more information.
"""

__version__      = '0.1.0'
__author__       = 'John Thorvald Wodder II'
__author_email__ = 'click-loglevel@varonathe.org'
__license__      = 'MIT'
__url__          = 'https://github.com/jwodder/click-loglevel'

import logging
import click

__all__ = ['LogLevelType']

class LogLevelType(click.ParamType):
    """
    A Click parameter type that accepts the standard logging level names (case
    insensitive) and converts them to their corresponding numeric values.  It
    also accepts integer values and leaves them as-is.
    """

    name = "log-level"
    LEVELS = ["NOTSET", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

    def convert(self, value, param, ctx):
        try:
            return int(value)
        except ValueError:
            vupper = value.upper()
            if vupper in self.LEVELS:
                return getattr(logging, vupper)
            else:
                self.fail(f"{value!r}: invalid log level", param, ctx)

    def get_metavar(self, param):
        return "[" + "|".join(self.LEVELS) + "]"

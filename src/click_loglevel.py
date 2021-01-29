"""
Log level parameter type for Click

Visit <https://github.com/jwodder/click-loglevel> for more information.
"""

__version__      = '0.1.0.dev1'
__author__       = 'John Thorvald Wodder II'
__author_email__ = 'click-loglevel@varonathe.org'
__license__      = 'MIT'
__url__          = 'https://github.com/jwodder/click-loglevel'

import logging
import click

class LogLevelType(click.ParamType):
    name = "log-level"
    LEVELS = ["NOTSET", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

    def convert(self, value, param, ctx):
        if value is None:
            return value
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

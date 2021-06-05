"""
Log level parameter type for Click

``click-loglevel`` provides a ``LogLevel`` parameter type for use in Click_
programs that wish to let the user set the logging level.  It accepts all of
the ``logging`` log level names (``CRITICAL``, ``ERROR``, ``WARNING``,
``INFO``, ``DEBUG``, and ``NOTSET``, all case insensitive), and converts them
into their corresponding numeric values.  It also accepts integer values and
leaves them as-is.  Custom log levels are also supported.

Starting in version 0.4.0, if you're using this package with Click 8, shell
completion of log level names (both built-in and custom) is also supported.

.. _Click: https://palletsprojects.com/p/click/

Visit <https://github.com/jwodder/click-loglevel> for more information.
"""

__version__      = '0.4.0.post1'
__author__       = 'John Thorvald Wodder II'
__author_email__ = 'click-loglevel@varonathe.org'
__license__      = 'MIT'
__url__          = 'https://github.com/jwodder/click-loglevel'

from   collections.abc import Mapping
import logging
import click

__all__ = ['LogLevel', 'LogLevelType']

class LogLevel(click.ParamType):
    """
    A Click parameter type that accepts the standard logging level names (case
    insensitive) and converts them to their corresponding numeric values.  It
    also accepts integer values and leaves them as-is.

    Custom log levels can be added by passing them as the ``extra`` argument to
    the constructor.  ``extra`` can be either an iterable of level names (in
    which case the levels must have already been defined — typically at the
    module level — by calling ``logging.addLevelName()``) or a mapping from
    level names to their corresponding values.  All custom log levels will be
    recognized case insensitively; if two different level names differ only in
    case, the result is undefined.
    """

    name = "log-level"
    LEVELS = ["NOTSET", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

    def __init__(self, extra=None):
        self.levels = {lv: getattr(logging, lv) for lv in self.LEVELS}
        level_names = list(self.LEVELS)
        if extra is not None:
            if isinstance(extra, Mapping):
                for lv, value in extra.items():
                    self.levels[lv.upper()] = value
                level_names.extend(extra.keys())
            else:
                for lv in extra:
                    self.levels[lv.upper()] = logging.getLevelName(lv)
                    level_names.append(lv)
        self.metavar = "[" + "|".join(level_names) + "]"

    def convert(self, value, param, ctx):
        try:
            return int(value)
        except ValueError:
            try:
                return self.levels[value.upper()]
            except KeyError:
                self.fail(f"{value!r}: invalid log level", param, ctx)

    def get_metavar(self, _param):
        return self.metavar

    def shell_complete(self, _ctx, _param, incomplete):
        from click.shell_completion import CompletionItem
        return [CompletionItem(c) for c in self.get_completions(incomplete)]

    def get_completions(self, incomplete):
        incomplete = incomplete.upper()
        for lv in self.levels:
            if lv.startswith(incomplete):
                yield lv


LogLevelType = LogLevel

from __future__ import annotations
from collections.abc import Iterable, Mapping
import asyncclick
from asyncclick.shell_completion import CompletionItem
from .core import LevelParser


class AsyncLogLevel(asyncclick.ParamType):
    """
    An AsyncClick parameter type that accepts the standard logging level names
    (case insensitive) and converts them to their corresponding numeric values.
    It also accepts integer values and leaves them as-is.

    Custom log levels can be added by passing them as the ``extra`` argument to
    the constructor.  ``extra`` can be either an iterable of level names (in
    which case the levels must have already been defined — typically at the
    module level — by calling ``logging.addLevelName()``) or a mapping from
    level names to their corresponding values.  All custom log levels will be
    recognized case insensitively; if two different level names differ only in
    case, the result is undefined.
    """

    name = "log-level"

    def __init__(self, extra: Iterable[str] | Mapping[str, int] | None = None) -> None:
        self.parser = LevelParser(extra)

    def convert(
        self,
        value: str | int,
        param: asyncclick.Parameter | None,
        ctx: asyncclick.Context | None,
    ) -> int:
        try:
            return int(value)
        except ValueError:
            assert isinstance(value, str)
            try:
                return self.parser.parse(value)
            except KeyError:
                self.fail(f"{value!r}: invalid log level", param, ctx)

    def get_metavar(
        self,
        param: asyncclick.Parameter,  # noqa: U100
        ctx: asyncclick.Context | None = None,  # noqa: U100
    ) -> str:
        return self.parser.metavar

    def shell_complete(
        self, _ctx: asyncclick.Context, _param: asyncclick.Parameter, incomplete: str
    ) -> list[CompletionItem]:
        return [CompletionItem(c) for c in self.parser.get_completions(incomplete)]

from __future__ import annotations
from collections.abc import Iterable, Iterator, Mapping
import logging

LEVELS = ["NOTSET", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


class LevelParser:
    def __init__(self, extra: Iterable[str] | Mapping[str, int] | None = None) -> None:
        self.levels: dict[str, int] = {lv: getattr(logging, lv) for lv in LEVELS}
        level_names = list(LEVELS)
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

    def parse(self, value: str) -> int:
        return self.levels[value.upper()]

    def get_completions(self, incomplete: str) -> Iterator[str]:
        incomplete = incomplete.upper()
        for lv in self.levels:
            if lv.startswith(incomplete):
                yield lv

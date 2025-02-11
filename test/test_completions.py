from __future__ import annotations
import pytest
from click_loglevel import LogLevel


@pytest.mark.parametrize(
    "incomplete,completions",
    [
        ("IN", ["INFO"]),
        ("in", ["INFO"]),
        ("In", ["INFO"]),
        ("info", ["INFO"]),
        ("i", ["INFO"]),
        ("w", ["WARNING"]),
        ("n", ["NOTSET"]),
        ("D", ["DEBUG"]),
        ("E", ["ERROR"]),
        ("c", ["CRITICAL"]),
        ("Q", []),
        ("v", []),
        ("INFOS", []),
    ],
)
def test_get_completions(incomplete: str, completions: list[str]) -> None:
    ll = LogLevel()
    assert list(ll.get_completions(incomplete)) == completions


@pytest.mark.parametrize(
    "incomplete,completions",
    [
        ("IN", ["INFO"]),
        ("in", ["INFO"]),
        ("In", ["INFO"]),
        ("info", ["INFO"]),
        ("i", ["INFO"]),
        ("w", ["WARNING"]),
        ("n", ["NOTSET", "NOTICE"]),
        ("NOT", ["NOTSET", "NOTICE"]),
        ("NOTS", ["NOTSET"]),
        ("NOTI", ["NOTICE"]),
        ("D", ["DEBUG"]),
        ("E", ["ERROR"]),
        ("c", ["CRITICAL"]),
        ("Q", []),
        ("v", ["VERBOSE"]),
        ("INFOS", []),
    ],
)
def test_get_completions_extra(incomplete: str, completions: list[str]) -> None:
    ll = LogLevel(extra={"Verbose": 5, "Notice": 25})
    assert list(ll.get_completions(incomplete)) == completions

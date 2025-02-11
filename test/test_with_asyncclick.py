from __future__ import annotations
import logging
from pathlib import Path
import subprocess
import sys
import asyncclick as click
from asyncclick.testing import CliRunner
import pytest
from click_loglevel import LogLevel

DATA_DIR = Path(__file__).with_name("data")


@click.command()
@click.option("-l", "--log-level", type=LogLevel(), default=logging.INFO)
async def lvlcmd(log_level: int) -> None:
    click.echo(repr(log_level))


@click.command()
@click.option("-l", "--log-level", type=LogLevel())
async def lvlcmd_nodefault(log_level: int) -> None:
    click.echo(repr(log_level))


STANDARD_LEVELS = [
    ("CRITICAL", logging.CRITICAL),
    ("critical", logging.CRITICAL),
    ("cRiTiCaL", logging.CRITICAL),
    (logging.CRITICAL, logging.CRITICAL),
    ("ERROR", logging.ERROR),
    ("error", logging.ERROR),
    ("ErRoR", logging.ERROR),
    (logging.ERROR, logging.ERROR),
    ("WARNING", logging.WARNING),
    ("warning", logging.WARNING),
    ("WaRnInG", logging.WARNING),
    (logging.WARNING, logging.WARNING),
    ("INFO", logging.INFO),
    ("info", logging.INFO),
    ("iNfO", logging.INFO),
    (logging.INFO, logging.INFO),
    ("DEBUG", logging.DEBUG),
    ("debug", logging.DEBUG),
    ("dEbUg", logging.DEBUG),
    (logging.DEBUG, logging.DEBUG),
    ("NOTSET", logging.NOTSET),
    ("notset", logging.NOTSET),
    ("NoTsEt", logging.NOTSET),
    (logging.NOTSET, logging.NOTSET),
    (42, 42),
    (" 42 ", 42),
]


@pytest.mark.anyio
@pytest.mark.parametrize("loglevel,value", STANDARD_LEVELS)
async def test_loglevel(loglevel: str | int, value: int) -> None:
    r = await CliRunner().invoke(lvlcmd, ["-l", str(loglevel)])
    assert r.exit_code == 0, r.output
    assert r.output == str(value) + "\n"


@pytest.mark.anyio
async def test_loglevel_default() -> None:
    r = await CliRunner().invoke(lvlcmd)
    assert r.exit_code == 0, r.output
    assert r.output == str(logging.INFO) + "\n"


@pytest.mark.anyio
async def test_loglevel_no_default() -> None:
    r = await CliRunner().invoke(lvlcmd_nodefault)
    assert r.exit_code == 0, r.output
    assert r.output == "None\n"


@pytest.mark.anyio
@pytest.mark.xfail(True, reason="asyncclick doesn't honor get_metavar")
async def test_loglevel_help() -> None:
    r = await CliRunner().invoke(lvlcmd, ["--help"])
    assert r.exit_code == 0, r.output
    assert "--log-level [NOTSET|DEBUG|INFO|WARNING|ERROR|CRITICAL]" in r.output


@pytest.mark.anyio
@pytest.mark.parametrize(
    "value",
    [
        "x",
        "logging.INFO",
        "VERBOSE",
    ],
)
async def test_invalid_loglevel(value: str) -> None:
    r = await CliRunner().invoke(lvlcmd, ["--log-level", value])
    assert r.exit_code != 0, r.output
    assert f"{value!r}: invalid log level" in str(r)


@pytest.mark.parametrize(
    "loglevel,value",
    STANDARD_LEVELS
    + [
        ("VERBOSE", 15),
        ("verbose", 15),
        ("VeRbOsE", 15),
        ("NOTICE", 25),
        ("notice", 25),
        ("nOtIcE", 25),
    ],
)
@pytest.mark.parametrize("script", ["list-extra-async.py", "dict-extra-async.py"])
def test_loglevel_extra(loglevel: str | int, value: int, script: str) -> None:
    r = subprocess.run(
        [sys.executable, str(DATA_DIR / script), "--log-level", str(loglevel)],
        stdout=subprocess.PIPE,
        text=True,
    )
    assert r.returncode == 0
    assert r.stdout == str(value) + "\n"


@pytest.mark.xfail(True, reason="asyncclick doesn't honor get_metavar")
@pytest.mark.parametrize("script", ["list-extra-async.py", "dict-extra-async.py"])
def test_loglevel_extra_help(script: str) -> None:
    r = subprocess.run(
        [sys.executable, str(DATA_DIR / script), "--help"],
        stdout=subprocess.PIPE,
        text=True,
    )
    assert r.returncode == 0
    assert (
        "--log-level [NOTSET|DEBUG|INFO|WARNING|ERROR|CRITICAL|VERBOSE|NOTICE]"
        in r.stdout
    )


@pytest.mark.parametrize(
    "value",
    [
        "x",
        "logging.INFO",
        "VERBATIM",
    ],
)
@pytest.mark.parametrize("script", ["list-extra-async.py", "dict-extra-async.py"])
def test_invalid_loglevel_extra(value: str, script: str) -> None:
    r = subprocess.run(
        [sys.executable, str(DATA_DIR / script), "--log-level", value],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    assert r.returncode != 0
    assert f"{value!r}: invalid log level" in r.stderr


@pytest.mark.parametrize(
    "loglevel,value",
    STANDARD_LEVELS
    + [
        ("VERBOSE", 15),
        ("verbose", 15),
        ("VeRbOsE", 15),
        ("NOTICE", 25),
        ("notice", 25),
        ("nOtIcE", 25),
    ],
)
@pytest.mark.parametrize(
    "script",
    [
        "list-extra-nonupper-async.py",
        "dict-extra-nonupper-async.py",
    ],
)
def test_loglevel_extra_nonupper(loglevel: str | int, value: int, script: str) -> None:
    r = subprocess.run(
        [sys.executable, str(DATA_DIR / script), "--log-level", str(loglevel)],
        stdout=subprocess.PIPE,
        text=True,
    )
    assert r.returncode == 0
    assert r.stdout == str(value) + "\n"


@pytest.mark.xfail(True, reason="asyncclick doesn't honor get_metavar")
@pytest.mark.parametrize(
    "script",
    [
        "list-extra-nonupper-async.py",
        "dict-extra-nonupper-async.py",
    ],
)
def test_loglevel_extra_nonupper_help(script: str) -> None:
    r = subprocess.run(
        [sys.executable, str(DATA_DIR / script), "--help"],
        stdout=subprocess.PIPE,
        text=True,
    )
    assert r.returncode == 0
    assert (
        "--log-level [NOTSET|DEBUG|INFO|WARNING|ERROR|CRITICAL|Verbose|Notice]"
        in r.stdout
    )


@pytest.mark.parametrize(
    "value",
    [
        "x",
        "logging.INFO",
        "VERBATIM",
    ],
)
@pytest.mark.parametrize(
    "script",
    [
        "list-extra-nonupper-async.py",
        "dict-extra-nonupper-async.py",
    ],
)
def test_invalid_loglevel_extra_nonupper(value: str, script: str) -> None:
    r = subprocess.run(
        [sys.executable, str(DATA_DIR / script), "--log-level", value],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    assert r.returncode != 0
    assert f"{value!r}: invalid log level" in r.stderr

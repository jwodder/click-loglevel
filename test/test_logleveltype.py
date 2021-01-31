import logging
import click
from   click.testing  import CliRunner
import pytest
from   click_loglevel import LogLevelType

@click.command()
@click.option('-l', '--log-level', type=LogLevelType(), default=logging.INFO)
def lvlcmd(log_level):
    click.echo(repr(log_level))

@click.command()
@click.option('-l', '--log-level', type=LogLevelType())
def lvlcmd_nodefault(log_level):
    click.echo(repr(log_level))

@pytest.mark.parametrize('loglevel,value', [
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
])
def test_logleveltype(loglevel, value):
    r = CliRunner().invoke(lvlcmd, ["-l", str(loglevel)])
    assert r.exit_code == 0, r.output
    assert r.output == str(value) + "\n"

def test_logleveltype_default():
    r = CliRunner().invoke(lvlcmd)
    assert r.exit_code == 0, r.output
    assert r.output == str(logging.INFO) + "\n"

def test_logleveltype_no_default():
    r = CliRunner().invoke(lvlcmd_nodefault)
    assert r.exit_code == 0, r.output
    assert r.output == "None\n"

def test_logleveltype_help():
    r = CliRunner().invoke(lvlcmd, ["--help"])
    assert r.exit_code == 0, r.output
    assert "--log-level [NOTSET|DEBUG|INFO|WARNING|ERROR|CRITICAL]" in r.output

@pytest.mark.parametrize('value', [
    "x",
    "logging.INFO",
    "VERBOSE",
])
def test_invalid_logleveltype(value):
    r = CliRunner().invoke(lvlcmd, ["--log-level", value])
    assert r.exit_code != 0, r.output
    assert f"{value!r}: invalid log level" in r.output

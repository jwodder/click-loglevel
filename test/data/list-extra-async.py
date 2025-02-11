import logging
import asyncclick as click
from click_loglevel import LogLevel

logging.addLevelName(15, "VERBOSE")
logging.addLevelName(25, "NOTICE")


@click.command()
@click.option("-l", "--log-level", type=LogLevel(extra=["VERBOSE", "NOTICE"]))
async def main(log_level: int) -> None:
    click.echo(repr(log_level))


if __name__ == "__main__":
    main()

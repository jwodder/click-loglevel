import logging
import click
from click_loglevel import LogLevel

logging.addLevelName(15, "Verbose")
logging.addLevelName(25, "Notice")


@click.command()
@click.option("-l", "--log-level", type=LogLevel(extra=["Verbose", "Notice"]))
def main(log_level: int) -> None:
    click.echo(repr(log_level))


if __name__ == "__main__":
    main()

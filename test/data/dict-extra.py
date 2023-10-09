import logging
import click
from click_loglevel import LogLevel


@click.command()
@click.option(
    "-l",
    "--log-level",
    type=LogLevel(extra={"VERBOSE": 15, "NOTICE": 25}),
)
def main(log_level: int) -> None:
    click.echo(repr(log_level))


if __name__ == "__main__":
    main()

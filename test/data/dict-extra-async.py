import logging
import asyncclick as click
from click_loglevel.asyncclick import AsyncLogLevel


@click.command()
@click.option(
    "-l",
    "--log-level",
    type=AsyncLogLevel(extra={"VERBOSE": 15, "NOTICE": 25}),
)
async def main(log_level: int) -> None:
    click.echo(repr(log_level))


if __name__ == "__main__":
    main()

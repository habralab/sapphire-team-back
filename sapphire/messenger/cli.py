import asyncio

import typer
from loguru import logger

from . import database
from .service import get_service
from .settings import Settings


@logger.catch
def run(ctx: typer.Context):
    loop: asyncio.AbstractEventLoop = ctx.obj["loop"]
    settings: Settings = ctx.obj["settings"]

    messenger_service = get_service(loop=loop, settings=settings)

    loop.run_until_complete(messenger_service.run())


def settings_callback(ctx: typer.Context):
    ctx.obj["settings"] = ctx.obj["settings"].messenger


def get_cli() -> typer.Typer:
    cli = typer.Typer()

    cli.callback()(settings_callback)
    cli.command(name="run")(run)
    cli.add_typer(database.get_cli(), name="database")

    return cli

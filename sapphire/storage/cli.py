import asyncio

import typer
from loguru import logger

from . import api, database
from .service import get_service
from .settings import Settings


@logger.catch
def run(ctx: typer.Context):
    loop: asyncio.AbstractEventLoop = ctx.obj["loop"]
    settings: Settings = ctx.obj["settings"]

    storage_service = get_service(
        api=api_service,
        database=database_service,
    )

    loop.run_until_complete(storage_service.run())


def settings_callback(ctx: typer.Context):
    ctx.obj["settings"] = ctx.obj["settings"].storage


def get_cli() -> typer.Typer:
    cli = typer.Typer()

    cli.callback()(settings_callback)
    cli.command(name="run")(run)
    cli.add_typer(database.get_cli(), name="database")

    return cli

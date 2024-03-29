import asyncio

import typer
from loguru import logger

from collabry.common.utils.settings import get_settings

from . import database
from .service import get_service
from .settings import Settings


@logger.catch
def run(ctx: typer.Context):
    loop: asyncio.AbstractEventLoop = ctx.obj["loop"]
    settings: Settings = ctx.obj["settings"]

    storage_service = get_service(settings=settings)

    loop.run_until_complete(storage_service.run())


def callback(ctx: typer.Context):
    ctx.obj = ctx.obj or {}

    if "loop" not in ctx.obj:
        ctx.obj["loop"] = asyncio.get_event_loop()

    if settings := ctx.obj.get("settings"):
        ctx.obj["settings"] = settings.storage
    else:
        ctx.obj["settings"] = get_settings(Settings)


def get_cli() -> typer.Typer:
    cli = typer.Typer()

    cli.callback()(callback)
    cli.command(name="run")(run)
    cli.add_typer(database.get_cli(), name="database")

    return cli

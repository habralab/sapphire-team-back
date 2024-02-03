import asyncio

import typer
from loguru import logger

from .service import get_service
from .settings import Settings


@logger.catch
def run(ctx: typer.Context):
    loop: asyncio.AbstractEventLoop = ctx.obj["loop"]
    settings: Settings = ctx.obj["settings"]

    email_service = get_service(loop=loop, settings=settings)

    loop.run_until_complete(email_service.run())


def settings_callback(ctx: typer.Context):
    ctx.obj["settings"] = ctx.obj["settings"].email


def get_cli() -> typer.Typer:
    cli = typer.Typer()

    cli.callback()(settings_callback)
    cli.command(name="run")(run)

    return cli

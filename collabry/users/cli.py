import asyncio

import typer
from loguru import logger

from collabry.common.utils.settings import get_settings

from .service import get_service
from .settings import Settings


@logger.catch
def run(ctx: typer.Context):
    loop: asyncio.AbstractEventLoop = ctx.obj["loop"]
    settings: Settings = ctx.obj["settings"]

    users_service = get_service(loop=loop, settings=settings)

    loop.run_until_complete(users_service.run())


def callback(ctx: typer.Context):
    ctx.obj = ctx.obj or {}

    if "loop" not in ctx.obj:
        ctx.obj["loop"] = asyncio.get_event_loop()

    if settings := ctx.obj.get("settings"):
        ctx.obj["settings"] = settings.users
    else:
        ctx.obj["settings"] = get_settings(Settings, env_prefix="USERS__")


def get_cli() -> typer.Typer:
    cli = typer.Typer()

    cli.callback()(callback)
    cli.command(name="run")(run)

    return cli

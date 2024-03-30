import asyncio
import pathlib
from typing import Optional

import typer
from loguru import logger

from collabry.common.utils.settings import get_settings

from . import database, email, messenger, notifications, projects, storage, users
from .service import get_service
from .settings import Settings


@logger.catch
def run(ctx: typer.Context):
    loop: asyncio.AbstractEventLoop = ctx.obj["loop"]
    settings: Settings = ctx.obj["settings"]

    users_service = get_service(loop=loop, settings=settings)

    loop.run_until_complete(users_service.run())


def callback(
        ctx: typer.Context,
        env: Optional[pathlib.Path] = typer.Option(
            None,
            "--env", "-e",
            help="`.env` config file location",
        ),
):
    ctx.obj = ctx.obj or {}

    if "loop" not in ctx.obj:
        ctx.obj["loop"] = asyncio.get_event_loop()

    if settings := ctx.obj.get("settings"):
        ctx.obj["settings"] = settings.collabry
    else:
        ctx.obj["settings"] = get_settings(Settings, env_file=env, env_prefix="COLLABRY__")


def get_cli() -> typer.Typer:
    cli = typer.Typer()

    cli.callback()(callback)
    cli.command(name="run")(run)
    cli.add_typer(database.get_cli(), name="database")
    cli.add_typer(email.get_cli(), name="email")
    cli.add_typer(messenger.get_cli(), name="messenger")
    cli.add_typer(notifications.get_cli(), name="notifications")
    cli.add_typer(projects.get_cli(), name="projects")
    cli.add_typer(storage.get_cli(), name="storage")
    cli.add_typer(users.get_cli(), name="users")

    return cli

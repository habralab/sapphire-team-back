import asyncio

import typer
from loguru import logger

from sapphire.notifications.database.service import get_service as get_database_service
from sapphire.notifications.settings import NotificationsSettings

from .service import get_service


@logger.catch
def run(ctx: typer.Context):
    settings: NotificationsSettings = ctx.obj["settings"]

    database_service = get_database_service(settings=settings)
    service = get_service(database=database_service, settings=settings)

    asyncio.run(service.run())


def get_cli() -> typer.Typer:
    cli = typer.Typer()

    cli.command(name="run")(run)

    return cli

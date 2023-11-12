import asyncio

import typer
from loguru import logger

from sapphire.common.api.websocket.connection_storage.storage import get_storage
from sapphire.messenger.database.service import get_service as get_database_service
from sapphire.messenger.settings import MessengerSettings

from .service import get_service


@logger.catch
def run(ctx: typer.Context):
    settings: MessengerSettings = ctx.obj["settings"]

    loop = asyncio.get_event_loop()
    database_service = get_database_service(settings=settings)
    websocket_connection_storage = get_storage()
    service = get_service(
        loop=loop,
        database=database_service,
        websocket_connection_storage=websocket_connection_storage,
        settings=settings,
    )

    loop.run_until_complete(service.run())


def get_cli() -> typer.Typer:
    cli = typer.Typer()

    cli.command(name="run")(run)

    return cli

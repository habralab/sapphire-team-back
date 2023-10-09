import asyncio

import typer
from loguru import logger

from sapphire.common.api.websocket.connection_storage.storage import get_storage
from sapphire.common.jwt.methods import get_jwt_methods
from sapphire.notifications.database.service import get_service as get_database_service

from .service import get_service


@logger.catch
def run(ctx: typer.Context):
    settings = ctx.obj["settings"]

    database_service = get_database_service(settings=settings)
    jwt_methods = get_jwt_methods(settings=settings)
    websocket_connection_storage = get_storage()
    api_service = get_service(
        database=database_service,
        jwt_methods=jwt_methods,
        websocket_connection_storage=websocket_connection_storage,
        settings=settings,
    )

    asyncio.run(api_service.run())



def get_cli() -> typer.Typer:
    cli = typer.Typer()

    cli.command(name="run")(run)

    return cli

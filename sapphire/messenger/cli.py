import asyncio

import typer
from loguru import logger

from sapphire.common.api.websocket.connection_storage.storage import get_storage
from sapphire.common.jwt.methods import get_jwt_methods

from . import api, broker, database
from .service import get_service
from .settings import get_settings


@logger.catch
def run(ctx: typer.Context):
    settings = ctx.obj["settings"]

    loop = asyncio.new_event_loop()
    database_service = database.get_service(settings=settings)
    jwt_methods = get_jwt_methods(settings=settings)
    websocket_connection_storage = get_storage()
    api_service = api.get_service(
        database=database_service,
        jwt_methods=jwt_methods,
        settings=settings,
    )
    broker_service = broker.get_service(
        loop=loop,
        database=database_service,
        websocket_connection_storage=websocket_connection_storage,
        settings=settings,
    )
    messenger_service = get_service(api=api_service, broker=broker_service)

    loop.run_until_complete(messenger_service.run())


def settings_callback(ctx: typer.Context):
    ctx.obj = ctx.obj or {}
    ctx.obj["settings"] = get_settings()


def get_cli() -> typer.Typer:
    cli = typer.Typer()

    cli.callback()(settings_callback)
    cli.command(name="run")(run)
    cli.add_typer(api.get_cli(), name="api")
    cli.add_typer(broker.get_cli(), name="broker")
    cli.add_typer(database.get_cli(), name="database")

    return cli

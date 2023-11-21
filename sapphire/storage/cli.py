import asyncio

import typer
from loguru import logger

from . import api, database, internal_api
from .service import get_service
from .settings import get_settings


@logger.catch
def run(ctx: typer.Context):
    settings = ctx.obj["settings"]

    loop = asyncio.get_event_loop()
    database_service = database.get_service(settings=settings)
    api_service = api.get_service(
        database=database_service,
        settings=settings,
    )
    internal_api_service = internal_api.get_service(database=database_service, settings=settings)
    storage_service = get_service(
        api=api_service,
        internal_api=internal_api_service,
        database=database_service,
    )

    loop.run_until_complete(storage_service.run())


def settings_callback(ctx: typer.Context):
    ctx.obj = ctx.obj or {}
    ctx.obj["settings"] = get_settings()


def get_cli() -> typer.Typer:
    cli = typer.Typer()

    cli.callback()(settings_callback)
    cli.command(name="run")(run)
    cli.add_typer(api.get_cli(), name="api")
    cli.add_typer(database.get_cli(), name="database")
    cli.add_typer(internal_api.get_cli(), name="internal-api")

    return cli

import asyncio

import typer
from loguru import logger

from sapphire.common.jwt.methods import get_jwt_methods

from . import api, broker, database
from .service import get_service
from .settings import ProjectsSettings, get_settings


@logger.catch
def run(ctx: typer.Context):
    settings: ProjectsSettings = ctx.obj["settings"]

    loop = asyncio.get_event_loop()
    database_service = database.get_service(settings=settings)
    jwt_methods = get_jwt_methods(settings=settings)
    api_service = api.get_service(
        database=database_service,
        jwt_methods=jwt_methods,
        settings=settings,
    )
    broker_service = broker.get_service(loop=loop, settings=settings)
    projects_service = get_service(api=api_service, broker=broker_service)

    loop.run_until_complete(projects_service.run())


def settings_callback(ctx: typer.Context):
    ctx.obj = ctx.obj or {}
    ctx.obj["settings"] = get_settings()


def get_cli() -> typer.Typer:
    cli = typer.Typer()

    cli.callback()(settings_callback)
    cli.command(name="run")(run)
    cli.add_typer(api.get_cli(), name="api")
    cli.add_typer(database.get_cli(), name="database")

    return cli

import asyncio

import typer
from loguru import logger

from sapphire.common.jwt import get_jwt_methods
from sapphire.projects.database import get_service as get_database_service
from sapphire.projects.broker.service import get_service as get_broker_service

from .service import get_service


@logger.catch
def run(ctx: typer.Context):
    settings = ctx.obj["settings"]

    loop = asyncio.get_event_loop()
    database_service = get_database_service(settings=settings)
    jwt_methods = get_jwt_methods(settings=settings)
    broker_service = get_broker_service(loop=loop, settings=settings)
    api_service = get_service(
        database=database_service,
        jwt_methods=jwt_methods,
        settings=settings,
        broker_service=broker_service
    )

    loop.run_until_complete(api_service.run())


def get_cli() -> typer.Typer:
    cli = typer.Typer()

    cli.command(name="run")(run)

    return cli

import asyncio

import typer
from loguru import logger

from .service import get_service
from .settings import get_settings


@logger.catch
def run(ctx: typer.Context):
    loop = asyncio.get_event_loop()
    settings = get_settings()
    email_service = get_service(loop=loop, settings=settings)

    loop.run_until_complete(email_service.run())


def get_cli() -> typer.Typer:
    cli = typer.Typer()

    cli.command(name="run")(run)

    return cli

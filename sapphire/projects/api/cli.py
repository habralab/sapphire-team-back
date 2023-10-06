import asyncio

import typer
from loguru import logger

from .service import get_service


@logger.catch
def serve(ctx: typer.Context):
    settings = ctx.obj["settings"]

    users_service = get_service(settings=settings)

    asyncio.run(users_service.run())


def get_cli() -> typer.Typer:
    cli = typer.Typer()

    cli.command(name="serve")(serve)

    return cli

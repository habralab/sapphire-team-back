import asyncio

import typer
from loguru import logger

from sapphire.email.sender import get_service as get_sender_service
from sapphire.email.settings import EmailSettings

from .service import get_service


@logger.catch
def run(ctx: typer.Context):
    settings: EmailSettings = ctx.obj["settings"]

    loop = asyncio.get_event_loop()
    sender_service = get_sender_service(settings=settings)
    broker_service = get_service(loop=loop, sender=sender_service, settings=settings)

    loop.run_until_complete(broker_service.run())


def get_cli() -> typer.Typer:
    cli = typer.Typer()

    cli.command(name="run")(run)

    return cli

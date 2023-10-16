import asyncio

import typer
from loguru import logger

from . import broker, sender
from .service import get_service
from .settings import EmailSettings, get_settings


@logger.catch
def run(ctx: typer.Context):
    settings: EmailSettings = ctx.obj["settings"]

    loop = asyncio.get_event_loop()
    sender_service = sender.get_service(settings=settings)
    broker_service = broker.get_service(loop=loop, sender=sender_service, settings=settings)
    email_service = get_service(broker=broker_service, sender=sender_service)

    loop.run_until_complete(email_service.run())


def settings_callback(ctx: typer.Context):
    ctx.obj = ctx.obj or {}
    ctx.obj["settings"] = get_settings()


def get_cli() -> typer.Typer:
    cli = typer.Typer()

    cli.callback()(settings_callback)
    cli.command(name="run")(run)
    cli.add_typer(broker.get_cli(), name="broker")

    return cli

import asyncio

import typer
from loguru import logger

from .settings import get_settings


@logger.catch
def run(ctx: typer.Context):
    pass


def settings_callback(ctx: typer.Context):
    ctx.obj = ctx.obj or {}
    ctx.obj["settings"] = get_settings()


def get_cli() -> typer.Typer:
    cli = typer.Typer()

    cli.callback()(settings_callback)
    cli.command(name="run")(run)

    return cli

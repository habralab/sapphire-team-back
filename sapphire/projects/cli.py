# pylint: disable=duplicate-code
import typer

from . import api
from .settings import get_settings


def settings_callback(ctx: typer.Context):
    ctx.obj = ctx.obj or {}
    ctx.obj["settings"] = get_settings()


def get_cli() -> typer.Typer:
    cli = typer.Typer()

    cli.callback()(settings_callback)
    cli.add_typer(api.get_cli(), name="api")

    return cli

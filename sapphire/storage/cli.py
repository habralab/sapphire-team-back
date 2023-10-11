import typer

from . import api, database
from .settings import get_settings


def settings_callback(ctx: typer.Context):
    ctx.obj = ctx.obj or {}
    ctx.obj["settings"] = get_settings()


def get_cli() -> typer.Typer:
    cli = typer.Typer()

    cli.add_typer(api.get_cli(), name="api")
    cli.callback()(settings_callback)
    cli.add_typer(database.get_cli(), name="database")

    return cli

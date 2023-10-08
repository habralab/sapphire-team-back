import typer

from . import broker, database
from .settings import get_settings


def settings_callback(ctx: typer.Context):
    ctx.obj = ctx.obj or {}
    ctx.obj["settings"] = get_settings()


def get_cli() -> typer.Typer:
    cli = typer.Typer()

    cli.callback()(settings_callback)
    cli.add_typer(broker.get_cli(), name="broker")
    cli.add_typer(database.get_cli(), name="database")

    return cli

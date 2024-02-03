import typer

from sapphire.common.database.cli import get_fixtures_cli, get_migrations_cli


def service_callback(ctx: typer.Context):
    ctx.obj["settings"] = ctx.obj["settings"].database


def get_cli() -> typer.Typer:
    cli = typer.Typer()

    cli.callback()(service_callback)
    cli.add_typer(get_fixtures_cli(), name="fixtures")
    cli.add_typer(get_migrations_cli(), name="migrations")

    return cli

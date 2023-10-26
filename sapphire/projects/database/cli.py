import typer

from sapphire.common.database.cli import get_fixtures_cli, get_migrations_cli
from .service import get_service


def service_callback(ctx: typer.Context):
    settings = ctx.obj["settings"]
    database_service = get_service(settings=settings)

    ctx.obj["database"] = database_service


def get_cli() -> typer.Typer:
    cli = typer.Typer()

    cli.callback()(service_callback)
    cli.add_typer(get_fixtures_cli(), name="fixtures")
    cli.add_typer(get_migrations_cli(), name="migrations")

    return cli

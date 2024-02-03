import typer

from sapphire.common.database.cli import get_fixtures_cli, get_migrations_cli

from .service import get_service
from .settings import get_settings


def service_callback(ctx: typer.Context):
    settings = get_settings()
    database_servise = get_service(settings=settings)
    ctx.obj["database"] = database_servise


def get_cli() -> typer.Typer:
    cli = typer.Typer()

    cli.callback()(service_callback)
    cli.add_typer(get_fixtures_cli(), name="fixtures")
    cli.add_typer(get_migrations_cli(), name="migrations")

    return cli

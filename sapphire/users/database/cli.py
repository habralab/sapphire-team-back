import typer

from sapphire.common.database.cli import get_fixtures_cli, get_migrations_cli
from sapphire.common.utils.settings import get_settings
from .service import get_service
from .settings import Settings


def callback(ctx: typer.Context):
    ctx.obj = ctx.obj or {}

    if settings := ctx.obj.get("settings"):
        settings = settings.database
    else:
        settings = get_settings(Settings)
    database_service = get_service(settings=settings)

    ctx.obj["settings"] = settings
    ctx.obj["database"] = database_service


def get_cli() -> typer.Typer:
    cli = typer.Typer(name="Database")

    cli.callback()(callback)
    cli.add_typer(get_fixtures_cli(), name="fixtures")
    cli.add_typer(get_migrations_cli(), name="migrations")

    return cli

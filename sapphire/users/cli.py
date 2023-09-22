import asyncio
import typer

from .database.service import get_service as get_database_service
from .service import get_service
from .settings import get_settings


def settings_callback(ctx: typer.Context):
    ctx.obj = ctx.obj or {}
    ctx.obj["settings"] = get_settings()


def serve(ctx: typer.Context):
    settings = ctx.obj["settings"]

    database_service = get_database_service(settings=settings.database)
    users_service = get_service(database=database_service, settings=settings)

    asyncio.run(users_service.run())


def get_cli() -> typer.Typer:
    cli = typer.Typer()

    cli.callback()(settings_callback)
    cli.command(name="serve")(serve)

    return cli

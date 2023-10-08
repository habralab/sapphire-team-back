from typing import Optional

import typer
from loguru import logger

from .service import get_service


@logger.catch
def migrate(ctx: typer.Context):
    database_service = ctx.obj["database"]
    database_service.migrate()


@logger.catch
def create(ctx: typer.Context,
           message: Optional[str] = typer.Option(
               None, "-m", "--message",
               help="Migration short message",
           )):
    database_service = ctx.obj["database"]
    database_service.create_migration(message=message)


def get_migration_cli() -> typer.Typer:
    cli = typer.Typer()

    cli.command(name="migrate")(migrate)
    cli.command(name="create")(create)

    return cli


def service_callback(ctx: typer.Context):
    settings = ctx.obj["settings"]
    database_service = get_service(settings=settings)

    ctx.obj["database"] = database_service


def get_cli() -> typer.Typer:
    cli = typer.Typer()

    cli.callback()(service_callback)
    cli.add_typer(get_migration_cli(), name="migrations")

    return cli

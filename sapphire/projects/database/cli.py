# pylint: disable=duplicate-code
import asyncio

import typer

from .service import get_service


def run_migration(settings, create=False, migrate=False):
    migration_service = get_service(settings=settings)
    if create:
        migration_service.create_migration()
    elif migrate:
        migration_service.migrate()
    asyncio.run(migration_service.run())


def migrate(ctx: typer.Context):
    settings = ctx.obj["settings"]
    run_migration(settings)


def create(ctx: typer.Context):
    settings = ctx.obj["settings"]
    run_migration(settings)


def get_cli() -> typer.Typer:
    cli = typer.Typer()

    cli.command(name="migrate")(migrate)
    cli.command(name="create_migration")(create)

    return cli

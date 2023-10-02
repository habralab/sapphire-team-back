# pylint: disable=duplicate-code
import asyncio

import typer

from sapphire.common.database.service import BaseDatabaseService


def run_migration(settings, create_migration=False, migrate=False):
    migration = BaseDatabaseService(dsn=settings)
    if create_migration:
        migration.create_migration()
    elif migrate:
        migration.migrate()
    asyncio.run(migration.run())


def migrate(ctx: typer.Context):
    settings = ctx.obj["settings"]
    run_migration(settings)


def create_migration(ctx: typer.Context):
    settings = ctx.obj["settings"]
    run_migration(settings)


def get_cli() -> typer.Typer:
    cli = typer.Typer()

    cli.command(name="migrate")(migrate)
    cli.command(name="create_migration")(create_migration)

    return cli

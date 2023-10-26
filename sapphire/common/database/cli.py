import asyncio
from typing import Optional

import typer
from loguru import logger
from rich.console import Console
from rich.table import Table

from sapphire.common.database.service import FixtureFormatEnum

from .service import BaseDatabaseService


@logger.catch
def migrations_list(ctx: typer.Context):
    database_service: BaseDatabaseService = ctx.obj["database"]

    database_service.show_migrations()


@logger.catch
def migrations_migrate(ctx: typer.Context):
    database_service: BaseDatabaseService = ctx.obj["database"]

    database_service.migrate()


@logger.catch
def migrations_rollback(
    ctx: typer.Context,
    revision: Optional[str] = typer.Argument(
        None,
        help="Revision id or relative revision (`-1`, `-2`)",
    ),
):
    database_service: BaseDatabaseService = ctx.obj["database"]

    database_service.rollback(revision=revision)


@logger.catch
def migrations_create(
        ctx: typer.Context,
        message: Optional[str] = typer.Option(
            None,
            "-m", "--message",
            help="Migration short message",
        ),
):
    database_service: BaseDatabaseService = ctx.obj["database"]

    database_service.create_migration(message=message)


def get_migrations_cli() -> typer.Typer:
    cli = typer.Typer(name="Migration")

    cli.command(name="migrate")(migrations_migrate)
    cli.command(name="rollback")(migrations_rollback)
    cli.command(name="create")(migrations_create)
    cli.command(name="list")(migrations_list)

    return cli


@logger.catch
def fixtures_list(ctx: typer.Context):
    database_service = ctx.obj["database"]

    fixtures = database_service.get_fixtures()

    table = Table("Name", "Format")
    for fixture in fixtures:
        table.add_row(fixture.name, fixture.format.value)
    Console().print(table)


@logger.catch
def fixtures_apply(
    ctx: typer.Context,
    name: str = typer.Argument(..., help="Fixture name"),
    fixture_format: FixtureFormatEnum = typer.Option(
        FixtureFormatEnum.YAML,
        "-f", "--format",
        help="Fixture format/extension",
    ),
):
    database_service = ctx.obj["database"]

    asyncio.run(database_service.apply_fixture(name=name, fixture_format=fixture_format))


def get_fixtures_cli() -> typer.Typer:
    cli = typer.Typer()

    cli.command(name="list")(fixtures_list)
    cli.command(name="apply")(fixtures_apply)

    return cli

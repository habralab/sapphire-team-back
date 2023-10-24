import asyncio
from typing import Optional

import typer
from loguru import logger
from rich.console import Console
from rich.table import Table

from sapphire.common.database.service import FixtureFormatEnum
from .service import get_service


@logger.catch
def migrate(ctx: typer.Context):
    database_service = ctx.obj["database"]

    database_service.migrate()


@logger.catch
def create_migration(
    ctx: typer.Context,
    message: Optional[str] = typer.Option(
        None, "-m", "--message", help="Migration short message"
    ),
):
    database_service = ctx.obj["database"]

    database_service.create_migration(message=message)


def get_migrations_cli() -> typer.Typer:
    cli = typer.Typer()

    cli.command(name="create")(create_migration)
    cli.command(name="migrate")(migrate)

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
def apply_fixture(
    ctx: typer.Context,
    name: str = typer.Argument(..., help="Fixture name"),
    format: FixtureFormatEnum = typer.Option(FixtureFormatEnum.YAML,
                                             help="Fixture format/extension"),
):
    database_service = ctx.obj["database"]

    asyncio.run(database_service.apply_fixture(name=name, format=format))


def get_fixtures_cli() -> typer.Typer:
    cli = typer.Typer()

    cli.command(name="list")(fixtures_list)
    cli.command(name="apply")(apply_fixture)

    return cli


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

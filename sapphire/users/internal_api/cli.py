import asyncio

import typer

from sapphire.users import database

from .service import get_service


def run(ctx: typer.Context):
    settings = ctx.obj["settings"]

    loop = asyncio.get_event_loop()
    database_service = database.get_service(settings=settings)
    internal_api_service = get_service(
        database=database_service,
        settings=settings,
    )

    loop.run_until_complete(internal_api_service.run())


def get_cli() -> typer.Typer:
    cli = typer.Typer()

    cli.command(name="run")(run)

    return cli

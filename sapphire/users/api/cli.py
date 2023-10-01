# pylint: disable=duplicate-code
import asyncio

import typer

from sapphire.users import database
from sapphire.users.oauth2 import habr

from .service import get_service


def serve(ctx: typer.Context):
    settings = ctx.obj["settings"]

    habr_oauth2 = habr.get_oauth2_backend(settings=settings)
    database_service = database.get_service(settings=settings)
    users_service = get_service(
        database=database_service,
        habr_oauth2=habr_oauth2,
        settings=settings,
    )

    asyncio.run(users_service.run())


def get_cli() -> typer.Typer:
    cli = typer.Typer()

    cli.command(name="serve")(serve)

    return cli
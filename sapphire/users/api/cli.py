import asyncio

import typer
from loguru import logger

from sapphire.common import jwt
from sapphire.common.habr.client import get_habr_client
from sapphire.common.habr_career.client import get_habr_career_client
from sapphire.users import database
from sapphire.users.oauth2 import habr
from sapphire.users.settings import UsersSettings

from .service import get_service


@logger.catch
def run(ctx: typer.Context):
    settings: UsersSettings = ctx.obj["settings"]

    habr_oauth2 = habr.get_oauth2_backend(settings=settings)
    habr_client = get_habr_client(settings=settings)
    habr_career_client = get_habr_career_client(settings=settings)
    jwt_methods = jwt.get_jwt_methods(settings=settings)
    database_service = database.get_service(settings=settings)
    api_service = get_service(
        database=database_service,
        habr_oauth2=habr_oauth2,
        habr_client=habr_client,
        habr_career_client=habr_career_client,
        jwt_methods=jwt_methods,
        settings=settings,
    )

    asyncio.run(api_service.run())


def get_cli() -> typer.Typer:
    cli = typer.Typer()

    cli.command(name="run")(run)

    return cli

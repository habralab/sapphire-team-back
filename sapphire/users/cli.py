import asyncio

import typer
from loguru import logger

from sapphire.common.habr.client import get_habr_client
from sapphire.common.habr_career.client import get_habr_career_client
from sapphire.common.jwt.methods import get_jwt_methods

from . import api, cache, database, internal_api
from .oauth2.habr import get_oauth2_backend
from .service import get_service
from .settings import UsersSettings, get_settings


@logger.catch
def run(ctx: typer.Context):
    settings: UsersSettings = ctx.obj["settings"]

    loop = asyncio.get_event_loop()
    database_service = database.get_service(settings=settings)
    habr_oauth2 = get_oauth2_backend(settings=settings)
    habr_client = get_habr_client(settings=settings)
    habr_career_client = get_habr_career_client(settings=settings)
    jwt_methods = get_jwt_methods(settings=settings)
    cache_service = cache.get_service(settings=settings)
    api_service = api.get_service(
        database=database_service,
        habr_oauth2=habr_oauth2,
        habr_client=habr_client,
        habr_career_client=habr_career_client,
        jwt_methods=jwt_methods,
        settings=settings,
        cache=cache_service
    )
    internal_api_service = internal_api.get_service(database=database_service, settings=settings)
    users_service = get_service(api=api_service, internal_api=internal_api_service)

    loop.run_until_complete(users_service.run())


def settings_callback(ctx: typer.Context):
    ctx.obj = ctx.obj or {}
    ctx.obj["settings"] = get_settings()


def get_cli() -> typer.Typer:
    cli = typer.Typer()

    cli.callback()(settings_callback)
    cli.command(name="run")(run)
    cli.add_typer(api.get_cli(), name="api")
    cli.add_typer(database.get_cli(), name="database")
    cli.add_typer(internal_api.get_cli(), name="internal-api")

    return cli

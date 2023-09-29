# pylint: disable=duplicate-code
import asyncio

import typer

from .service import get_service


def serve(ctx: typer.Context):
    settings = ctx.obj["settings"]

    users_service = get_service(settings=settings)

    asyncio.run(users_service.run())


def get_cli() -> typer.Typer:
    cli = typer.Typer()

    cli.command(name="serve")(serve)

    return cli

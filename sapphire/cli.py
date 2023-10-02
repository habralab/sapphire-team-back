import typer
from . import email, messenger, notifications, projects, storage, users


def get_cli() -> typer.Typer:
    cli = typer.Typer()

    cli.add_typer(email.get_cli(), name="email")
    cli.add_typer(messenger.get_cli(), name="messenger")
    cli.add_typer(notifications.get_cli(), name="notifications")
    cli.add_typer(projects.get_cli(), name="projects")
    cli.add_typer(storage.get_cli(), name="storage")
    cli.add_typer(users.get_cli(), name="users")

    return cli

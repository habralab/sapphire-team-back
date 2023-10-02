import typer
from sapphire.common.database.service import BaseDatabaseService
from pydantic import AnyUrl

app = typer.Typer()


@app.command(name='create_migration')
def create_migration(db_dsn: AnyUrl, message: str | None = None):
    service = BaseDatabaseService(db_dsn)
    service.create_migration(message)


@app.command(name='migrate')
def migrate(db_dsn: AnyUrl):
    service = BaseDatabaseService(db_dsn)
    service.migrate()


if __name__ == '__main__':
    app(db_dsn="sqlite+aiosqlite:///projects.sqlite3")

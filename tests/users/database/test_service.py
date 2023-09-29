import os
import pathlib

from sapphire.users.database.service import UsersDatabaseService


def test_get_alembic_config_path(database_service: UsersDatabaseService):
    expected_path = (
        pathlib.Path(os.curdir).absolute() / "sapphire" / "users" / "database" / "migrations"
    )

    path = database_service.get_alembic_config_path()

    assert isinstance(path, pathlib.Path)
    assert path == expected_path

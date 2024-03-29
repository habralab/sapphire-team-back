import pytest

from collabry.common.database.service import BaseDatabaseService


@pytest.fixture()
def database_service() -> BaseDatabaseService:
    return BaseDatabaseService(dsn="sqlite+aiosqlite:///test.db")

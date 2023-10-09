import pytest

from sapphire.users.database.service import UsersDatabaseService
from sapphire.users.settings import UsersSettings


@pytest.fixture()
def database_service(settings: UsersSettings) -> UsersDatabaseService:
    return UsersDatabaseService(dsn=str(settings.db_dsn))

@pytest.fixture()
def settings():
    return UsersSettings()

@pytest.fixture
async def async_session():
    session = AsyncSession()
    try:
        yield session
    finally:
        await session.close()

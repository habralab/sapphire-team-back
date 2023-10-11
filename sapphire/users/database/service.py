import pathlib
import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from sapphire.common.database.service import BaseDatabaseService
from sapphire.users.settings import UsersSettings

from .models import User


class UsersDatabaseService(BaseDatabaseService):
    def get_alembic_config_path(self) -> pathlib.Path:
        return pathlib.Path(__file__).parent / "migrations"

    async def update_user(self,
                          session: AsyncSession,
                          user_id: uuid.UUID,
                          first_name: str,
                          last_name: str):
        user = await session.get(User, user_id)
        if user:
            user.first_name = first_name
            user.last_name = last_name
            await session.commit()
        else:
            ValueError("User Not Found")


def get_service(settings: UsersSettings) -> UsersDatabaseService:
    return UsersDatabaseService(dsn=str(settings.db_dsn))

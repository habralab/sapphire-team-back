import pathlib
import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from sapphire.common.database.service import BaseDatabaseService
from sapphire.users.settings import UsersSettings

from .models import User


class UsersDatabaseService(BaseDatabaseService):
    def get_alembic_config_path(self) -> pathlib.Path:
        return pathlib.Path(__file__).parent / "migrations"

    async def get_user(self, session: AsyncSession, user_id: uuid.UUID):
        stmt = select(User).where(User.id == user_id)
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()
        return user

    async def update_user(
            self,
            session: AsyncSession,
            user: User,
            first_name: str,
            last_name: str,
    ):
        user.first_name = first_name
        user.last_name = last_name
        session.add(user)


def get_service(settings: UsersSettings) -> UsersDatabaseService:
    return UsersDatabaseService(dsn=str(settings.db_dsn))

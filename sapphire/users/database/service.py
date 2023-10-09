import pathlib
import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from sapphire.common.database.service import BaseDatabaseService
from sapphire.users.database.models import User
from sapphire.users.settings import UsersSettings


class UsersDatabaseService(BaseDatabaseService):
    def get_alembic_config_path(self) -> pathlib.Path:
        return pathlib.Path(__file__).parent / "migrations"

    async def get_user(
        self,
        session: AsyncSession,
        email: str
    ) -> User | None:
        user = await session.query(User).where(User.email == email).get_first()

        return user

    async def create_user(
        self,
        session: AsyncSession,
        user_id: uuid.UUID,
        email: str,
        first_name: str | None = None,
        last_name: str | None = None,
        avatar: str | None = None
    ) -> User:
        user = User(
            id=user_id, email=email, first_name=first_name, last_name=last_name, avatar=avatar
        )
        session.add(user)

        return user

    async def get_or_create_user(
        self,
        session: AsyncSession,
        user_id: uuid.UUID,
        email: str,
        first_name: str | None = None,
        last_name: str | None = None,
        avatar: str | None = None,
    ) -> User | None:
        user = await self.get_user(
            session=session,
            email=email
        )
        if not user:
            await self.create_user(
                session=session,
                user_id=user_id, email=email
            )
            return user

        return user


def get_service(settings: UsersSettings) -> UsersDatabaseService:
    return UsersDatabaseService(dsn=str(settings.db_dsn))

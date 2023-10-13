import pathlib
import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from sapphire.common.database.service import BaseDatabaseService
from sapphire.users.database.models import Profile, User
from sapphire.users.settings import UsersSettings

from .models import User


class UsersDatabaseService(BaseDatabaseService):
    def get_alembic_config_path(self) -> pathlib.Path:
        return pathlib.Path(__file__).parent / "migrations"

    async def get_user(
        self,
        session: AsyncSession,
        email: str,
    ) -> User | None:
        user = await session.execute(
            select(User).where(User.email == email)
        )

        return user.first()

    async def create_user(
        self,
        session: AsyncSession,
        user_id: uuid.UUID,
        email: str,
        first_name: str | None = None,
        last_name: str | None = None,
        avatar: str | None = None,
    ) -> User:
        user = User(
            id=user_id, email=email, first_name=first_name, last_name=last_name, avatar=avatar
        )
        session.add(user)
        self.create_profile(user=user, about=None)

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
            user = await self.create_user(
                session=session,
                user_id=user_id, email=email
            )

        return user

    async def create_profile(
        self,
        session: AsyncSession,
        user: User,
        about: str | None,
    ) -> Profile:
        profile = Profile(
            user_id=user.id,
            about=about
            )
        session.add(profile)

        return profile


def get_service(settings: UsersSettings) -> UsersDatabaseService:
    return UsersDatabaseService(dsn=str(settings.db_dsn))

import pathlib

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
    ):
        stmt = select(User).where(User.email == email)
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()

        return user

    async def update_user(
            self,
            session: AsyncSession,
            user: User,
            first_name: str,
            last_name: str,
    ) -> User:
        user.first_name = first_name
        user.last_name = last_name
        session.add(user)

        return user

    async def create_user(
            self,
            session: AsyncSession,
            email: str,
            first_name: str | None = None,
            last_name: str | None = None,
    ) -> User:
        user = User(
            email=email,
            first_name=first_name,
            last_name=last_name,
        )
        profile = Profile(user=user)
        user.profile = profile
        session.add_all([user, profile])

        return user

    async def get_or_create_user(
            self,
            session: AsyncSession,
            email: str,
            first_name: str | None = None,
            last_name: str | None = None,
    ) -> User:
        user = await self.get_user(session=session, email=email)
        if user is None:
            user = await self.create_user(
                session=session,
                email=email,
                first_name=first_name,
                last_name=last_name,
            )

        return user


def get_service(settings: UsersSettings) -> UsersDatabaseService:
    return UsersDatabaseService(dsn=str(settings.db_dsn))

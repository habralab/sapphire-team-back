import pathlib
import uuid
from typing import Type

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from sapphire.common.database.service import BaseDatabaseService
from sapphire.common.database.utils import Empty
from sapphire.users.database.models import Profile, User
from sapphire.users.settings import UsersSettings


class UsersDatabaseService(BaseDatabaseService):
    def get_alembic_config_path(self) -> pathlib.Path:
        return pathlib.Path(__file__).parent / "migrations"

    async def get_user(
            self,
            session: AsyncSession,
            user_id: uuid.UUID | Type[Empty] = Empty,
            email: str | Type[Empty] = Empty,
    ):
        filters = []
        if user_id is not Empty:
            filters.append(User.id == user_id)
        if email is not Empty:
            filters.append(User.email == email)

        stmt = select(User).where(*filters)
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()

        return user

    async def update_user(
            self,
            session: AsyncSession,
            user: User,
            first_name: str,
            last_name: str,
            main_specialization_id: uuid.UUID,
            secondary_specialization_id: uuid.UUID
    ) -> User:
        user.first_name = first_name
        user.last_name = last_name
        if user.profile:
            if main_specialization_id is not None:
                user.profile.main_specialization_id = main_specialization_id
            if secondary_specialization_id is not None:
                user.profile.secondary_specialization_id = secondary_specialization_id
        session.add(user)

        return user

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
        profile = Profile(
            user_id=user.id, about=None,
            )
        user.profile = profile
        session.add_all([user, profile])

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


def get_service(settings: UsersSettings) -> UsersDatabaseService:
    return UsersDatabaseService(dsn=str(settings.db_dsn))

import pathlib
import uuid
from typing import Type

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

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

        stmt = select(User).options(
            joinedload(User.profile), joinedload(User.skills),
        ).where(*filters)
        result = await session.execute(stmt)
        user = result.unique().scalar_one_or_none()

        return user

    async def update_user(
            self,
            session: AsyncSession,
            user: User,
            first_name: str | None | Type[Empty] = Empty,
            last_name: str | None | Type[Empty] = Empty,
            avatar: str | None | Type[Empty] = Empty,
            about: str | None | Type[Empty] = Empty,
            main_specialization_id: uuid.UUID | None | Type[Empty] = Empty,
            secondary_specialization_id: uuid.UUID | None | Type[Empty] = Empty,
    ) -> User:
        if first_name is not Empty:
            user.first_name = first_name
        if last_name is not Empty:
            user.last_name = last_name
        if avatar is not Empty:
            user.avatar = avatar
        if about is not Empty:
            user.profile.about = about
        if main_specialization_id is not Empty:
            user.profile.main_specialization_id = main_specialization_id
        if secondary_specialization_id is not Empty:
            user.profile.secondary_specialization_id = secondary_specialization_id
        session.add_all([user, user.profile])

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


def get_service(settings: UsersSettings) -> UsersDatabaseService:
    return UsersDatabaseService(dsn=str(settings.db_dsn))

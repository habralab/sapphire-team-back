import pathlib
import uuid
from typing import Type

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from sapphire.common.database.service import BaseDatabaseService
from sapphire.common.database.utils import Empty
from sapphire.users.database.models import Profile, User, UserSkill
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
            first_name: str | None | Type[Empty] = Empty,
            last_name: str | None | Type[Empty] = Empty,
            avatar: str | None | Type[Empty] = Empty,
            main_specialization_id: uuid.UUID | None | Type[Empty] = Empty,
            secondary_specialization_id: uuid.UUID | None | Type[Empty] = Empty,
    ) -> User:
        if first_name is not Empty:
            user.first_name = first_name
        if last_name is not Empty:
            user.last_name = last_name
        if avatar is not Empty:
            user.avatar = avatar
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

    async def get_user_skills(self,
                              session: AsyncSession,
                              skill_id: uuid.UUID | Type[Empty] = Empty,
                              user: User | Type[Empty] = Empty,
                              ):
        filters = []
        if skill_id is not Empty:  # of if user is not Empty?
            filters.append(UserSkill.user_id == user.id)
        stmt = select(UserSkill.skill_id).where(*filters)
        result = await session.execute(stmt)
        current_skills = result.scalars().all()

        return current_skills

    async def update_user_skills(self,
                                 session: AsyncSession,
                                 new_userskills_ids: list[uuid.UUID] | None | Type[Empty],
                                 user: User,
                                 ):

        stmt = delete(UserSkill).where(UserSkill.user_id == user.id)
        await session.execute(stmt)

        if new_userskills_ids is not Empty:
            for new_skill_id in new_userskills_ids:
                new_skill = UserSkill(user_id=user.id, skill_id=new_skill_id)
                session.add(new_skill)
        return new_userskills_ids


def get_service(settings: UsersSettings) -> UsersDatabaseService:
    return UsersDatabaseService(dsn=str(settings.db_dsn))

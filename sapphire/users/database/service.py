import uuid
from typing import Set, Type

import bcrypt
from dill import session
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from sapphire.common.database.service import BaseDatabaseService
from sapphire.common.utils.empty import Empty
from sapphire.database.models import Profile, User, UserSkill

from .settings import Settings


class Service(BaseDatabaseService):  # pylint: disable=abstract-method
    def hash_user_password(self, password: str) -> str:
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        return hashed_password.decode("utf-8")

    def check_user_password(self, user: User, password: str) -> bool:
        if user.password is None:
            return False
        return bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8"))

    async def get_user(
            self,
            session: AsyncSession,
            user_id: uuid.UUID | Type[Empty] = Empty,
            email: str | Type[Empty] = Empty,
    ) -> User | None:
        filters = []
        if user_id is not Empty:
            filters.append(User.id == user_id)
        if email is not Empty:
            filters.append(User.email == email)

        stmt = select(User).where(*filters)
        result = await session.execute(stmt)
        user = result.unique().scalar_one_or_none()

        return user

    async def update_user(
            self,
            session: AsyncSession,
            user: User,
            password: str | Type[Empty] = Empty,
            first_name: str | None | Type[Empty] = Empty,
            last_name: str | None | Type[Empty] = Empty,
            avatar: str | None | Type[Empty] = Empty,
            about: str | None | Type[Empty] = Empty,
            main_specialization_id: uuid.UUID | None | Type[Empty] = Empty,
            secondary_specialization_id: uuid.UUID | None | Type[Empty] = Empty,
    ) -> User:
        if password is not Empty:
            user.password = self.hash_user_password(password)
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
            password: str | None = None,
            first_name: str | None = None,
            last_name: str | None = None,
    ) -> User:
        user = User(
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=None if password is None else self.hash_user_password(password),
        )
        profile = Profile(user=user)
        user.profile = profile
        session.add_all([user, profile])

        return user

    async def get_user_skills(
            self,
            session: AsyncSession,
            user: User | Type[Empty] = Empty,
    ) -> set[uuid.UUID]:
        filters = []
        if user is not Empty:
            filters.append(UserSkill.user == user)
        stmt = select(UserSkill.skill_id).where(*filters)
        result = await session.execute(stmt)

        current_skills = result.scalars().all()

        return set(current_skills)

    async def update_user_skills(self,
        session: AsyncSession,
        user: User,
        skills: Set[uuid.UUID] = frozenset(),
    ) -> Set[uuid.UUID]:
        async with session.begin_nested():
            user.skills = []
            session.add(user)

        async with session.begin_nested():
            new_skills = [UserSkill(user=user, skill_id=skill) for skill in skills]
            user.skills = new_skills
            session.add(user)

        return skills

    async def get_user_email(
            self,
            session: AsyncSession,
            email: str
    ) -> User:
        filters = []
        if email is not Empty:
            filters.append(User.email == email)

        stmt = select(User).where(*filters)
        result = await session.execute(stmt)
        current_email = result.scalar_one_or_none()
        return current_email


def get_service(settings: Settings) -> Service:
    return Service(dsn=str(settings.dsn))

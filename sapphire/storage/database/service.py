import pathlib
import uuid
from typing import Type

from sqlalchemy import desc, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from sapphire.common.database.service import BaseDatabaseService
from sapphire.common.utils.empty import Empty
from sapphire.storage.database.models import Base, Skill, Specialization, SpecializationGroup
from sapphire.storage.settings import StorageSettings


class StorageDatabaseService(BaseDatabaseService):
    def get_alembic_config_path(self) -> pathlib.Path:
        return pathlib.Path(__file__).parent / "migrations"

    def get_fixtures_directory_path(self) -> pathlib.Path | None:
        return pathlib.Path(__file__).parent / "fixtures"

    def get_models(self) -> list[Type[Base]]:
        return [Skill, Specialization, SpecializationGroup]

    async def _get_specializations_filters(
            self,
            query_text: str | Type[Empty] = Empty,
            group_id: uuid.UUID | Type[Empty] = Empty,
    ) -> list:
        filters = []
        if query_text is not Empty:
            filters.append(Specialization.name.contains(query_text))

        if group_id is not Empty:
            filters.append(Specialization.group_id == group_id)

        return filters

    async def get_specializations_count(
            self,
            session: AsyncSession,
            query_text: str | Type[Empty] = Empty,
            group_id: uuid.UUID | Type[Empty] = Empty,
    ) -> int:
        query = select(func.count(Specialization.id)) # pylint: disable=not-callable

        filters = await self._get_specializations_filters(query_text=query_text, group_id=group_id)

        query = query.where(*filters)
        result = await session.scalar(query)

        return result

    async def get_specializations(
            self,
            session: AsyncSession,
            query_text: str | Type[Empty] = Empty,
            group_id: uuid.UUID | Type[Empty] = Empty,
            page: int = 1,
            per_page: int = 10,
    ) -> list[Specialization]:
        query = select(Specialization).order_by(desc(Specialization.created_at))

        filters = await self._get_specializations_filters(query_text=query_text, group_id=group_id)

        query = query.where(*filters)

        offset = (page - 1) * per_page
        query = query.limit(per_page).offset(offset)

        specializations = await session.execute(query)

        return list(specializations.unique().scalars().all())

    async def get_specialization(
            self,
            session: AsyncSession,
            habr_id: int,
    ) -> Specialization | None:
        query = select(Specialization).where(Specialization.habr_id == habr_id)

        result = await session.execute(query)

        return result.unique().scalar_one_or_none()

    async def _get_specialization_groups_filters(
        self, query_text: str | Type[Empty] = Empty
    ) -> list:
        filters = []
        if query_text is not Empty:
            filters.append(or_(
                SpecializationGroup.name.contains(query_text),
                SpecializationGroup.name_en.contains(query_text),
            ))

        return filters

    async def get_specialization_groups_count(
        self,
        session: AsyncSession,
        query_text: str | Type[Empty] = Empty,
    ) -> int:
        query = (
            select(func.count(SpecializationGroup.id)) # pylint: disable=not-callable
            .order_by(desc(SpecializationGroup.created_at))
        )

        filters = await self._get_specialization_groups_filters(query_text=query_text)
        query = query.where(*filters)

        result = await session.scalar(query)

        return result

    async def get_specialization_groups(
        self,
        session: AsyncSession,
        query_text: str | Type[Empty] = Empty,
        page: int = 1,
        per_page: int = 10,
    ) -> list[SpecializationGroup]:
        query = select(SpecializationGroup).order_by(desc(SpecializationGroup.created_at))

        filters = await self._get_specialization_groups_filters(query_text=query_text)
        query = query.where(*filters)

        offset = (page - 1) * per_page
        query = query.limit(per_page).offset(offset)

        specialization_groups = await session.execute(query)

        return list(specialization_groups.unique().scalars().all())

    async def get_specialization_group(
            self,
            session: AsyncSession,
            habr_id: int,
    ) -> SpecializationGroup | None:
        query = select(SpecializationGroup).where(SpecializationGroup.habr_id == habr_id)

        result = await session.execute(query)

        return result.unique().scalar_one_or_none()

    async def _get_skills_filters(
        self,
        query_text: str | Type[Empty] = Empty,
        skill_ids: list[uuid.UUID] | Type[Empty] = Empty,
    ) -> list:
        filters = []
        if query_text is not Empty:
            filters.append(Skill.name.contains(query_text))
        if skill_ids is not Empty:
            filters.append(or_(*(Skill.id == id_ for id_ in skill_ids)))

        return filters

    async def get_skills_count(
        self,
        session: AsyncSession,
        query_text: str | Type[Empty] = Empty,
        skill_ids: list[uuid.UUID] | Type[Empty] = Empty,
    ) -> int:
        query = select(func.count(Skill.id)) # pylint: disable=not-callable

        filters = await self._get_skills_filters(query_text=query_text, skill_ids=skill_ids)

        query = query.where(*filters)
        result = await session.scalar(query)

        return result

    async def get_skills(
        self,
        session: AsyncSession,
        query_text: str | Type[Empty] = Empty,
        skill_ids: list[uuid.UUID] | Type[Empty] = Empty,
        page: int = 1,
        per_page: int = 10,
    ) -> list[Skill]:
        query = select(Skill).order_by(desc(Skill.created_at))

        filters = await self._get_skills_filters(query_text=query_text, skill_ids=skill_ids)

        query = query.where(*filters)
        skills = await session.execute(query)

        offset = (page - 1) * per_page
        query = query.limit(per_page).offset(offset)

        return list(skills.unique().scalars().all())

    async def get_skill(self, session: AsyncSession, habr_id: int) -> Skill | None:
        query = select(Skill).where(Skill.habr_id == habr_id)

        result = await session.execute(query)

        return result.unique().scalar_one_or_none()


def get_service(settings: StorageSettings) -> StorageDatabaseService:
    return StorageDatabaseService(dsn=str(settings.db_dsn))

import uuid
from typing import Type

from sqlalchemy import desc, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from sapphire.common.database.service import BaseDatabaseService
from sapphire.common.utils.empty import Empty
from sapphire.database.models import Skill, Specialization, SpecializationGroup

from .settings import Settings


class Service(BaseDatabaseService):  # pylint: disable=abstract-method
    async def _get_specializations_filters(
            self,
            query: str | Type[Empty] = Empty,
            group_id: uuid.UUID | Type[Empty] = Empty,
            specialization_ids: list[uuid.UUID] | Type[Empty] = Empty,
            exclude_specialization_ids: list[uuid.UUID] | Type[Empty] = Empty,
    ) -> list:
        filters = []
        if query is not Empty:
            filters.append(or_(
                Specialization.name.icontains(query),
                Specialization.name_en.icontains(query),
            ))

        if group_id is not Empty:
            filters.append(Specialization.group_id == group_id)

        if specialization_ids is not Empty:
            filters.append(or_(*(Specialization.id == id_ for id_ in specialization_ids)))

        if exclude_specialization_ids is not Empty:
            filters.append(Specialization.id.not_in(exclude_specialization_ids))

        return filters

    async def get_specializations_count(
            self,
            session: AsyncSession,
            query: str | Type[Empty] = Empty,
            specialization_ids: list[uuid.UUID] | Type[Empty] = Empty,
            exclude_specialization_ids: list[uuid.UUID] | Type[Empty] = Empty,
            group_id: uuid.UUID | Type[Empty] = Empty,
    ) -> int:
        statement = select(func.count(Specialization.id)) # pylint: disable=not-callable

        filters = await self._get_specializations_filters(
            query=query,
            group_id=group_id,
            specialization_ids=specialization_ids,
            exclude_specialization_ids=exclude_specialization_ids,
        )

        statement = statement.where(*filters)
        result = await session.scalar(statement)

        return result

    async def get_specializations(
            self,
            session: AsyncSession,
            query: str | Type[Empty] = Empty,
            group_id: uuid.UUID | Type[Empty] = Empty,
            specialization_ids: list[uuid.UUID] | Type[Empty] = Empty,
            exclude_specialization_ids: list[uuid.UUID] | Type[Empty] = Empty,
            page: int = 1,
            per_page: int = 10,
    ) -> list[Specialization]:
        statement = select(Specialization).order_by(desc(Specialization.created_at))

        filters = await self._get_specializations_filters(
            query=query,
            group_id=group_id,
            specialization_ids=specialization_ids,
            exclude_specialization_ids=exclude_specialization_ids,
        )

        statement = statement.where(*filters)

        offset = (page - 1) * per_page
        statement = statement.limit(per_page).offset(offset)

        specializations = await session.execute(statement)

        return list(specializations.unique().scalars().all())

    async def get_specialization(
            self,
            session: AsyncSession,
            habr_id: int,
    ) -> Specialization | None:
        statement = select(Specialization).where(Specialization.habr_id == habr_id)

        result = await session.execute(statement)

        return result.unique().scalar_one_or_none()

    async def _get_specialization_groups_filters(
            self,
            query: str | Type[Empty] = Empty,
            group_ids: list[uuid.UUID] | Type[Empty] = Empty,
            exclude_group_ids: list[uuid.UUID] | Type[Empty] = Empty,
    ) -> list:
        filters = []

        if query is not Empty:
            filters.append(or_(
                SpecializationGroup.name.icontains(query),
                SpecializationGroup.name_en.icontains(query),
            ))
        if group_ids is not Empty:
            filters.append(or_(*(SpecializationGroup.id == id_ for id_ in group_ids)))
        if exclude_group_ids is not Empty:
            filters.append(SpecializationGroup.id.not_in(exclude_group_ids))

        return filters

    async def get_specialization_groups_count(
        self,
        session: AsyncSession,
        query: str | Type[Empty] = Empty,
        group_ids: list[uuid.UUID] | Type[Empty] = Empty,
        exclude_group_ids: list[uuid.UUID] | Type[Empty] = Empty,
    ) -> int:
        statement = select(func.count(SpecializationGroup.id))  # pylint: disable=not-callable

        filters = await self._get_specialization_groups_filters(
            query=query,
            group_ids=group_ids,
            exclude_group_ids=exclude_group_ids,
        )
        statement = statement.where(*filters)

        result = await session.scalar(statement)

        return result

    async def get_specialization_groups(
        self,
        session: AsyncSession,
        query: str | Type[Empty] = Empty,
        group_ids: list[uuid.UUID] | Type[Empty] = Empty,
        exclude_group_ids: list[uuid.UUID] | Type[Empty] = Empty,
        page: int = 1,
        per_page: int = 10,
    ) -> list[SpecializationGroup]:
        statement = select(SpecializationGroup).order_by(desc(SpecializationGroup.created_at))

        filters = await self._get_specialization_groups_filters(
            query=query,
            group_ids=group_ids,
            exclude_group_ids=exclude_group_ids,
        )

        statement = statement.where(*filters)

        offset = (page - 1) * per_page
        statement = statement.limit(per_page).offset(offset)

        specialization_groups = await session.execute(statement)

        return list(specialization_groups.unique().scalars().all())

    async def get_specialization_group(
            self,
            session: AsyncSession,
            habr_id: int,
    ) -> SpecializationGroup | None:
        statement = select(SpecializationGroup).where(SpecializationGroup.habr_id == habr_id)

        result = await session.execute(statement)

        return result.unique().scalar_one_or_none()

    async def _get_skills_filters(
        self,
        query: str | Type[Empty] = Empty,
        skill_ids: list[uuid.UUID] | Type[Empty] = Empty,
        exclude_skill_ids: list[uuid.UUID] | Type[Empty] = Empty,
    ) -> list:
        filters = []

        if query is not Empty:
            filters.append(Skill.name.icontains(query))
        if skill_ids is not Empty:
            filters.append(or_(*(Skill.id == id_ for id_ in skill_ids)))
        if exclude_skill_ids is not Empty:
            filters.append(Skill.id.not_in(exclude_skill_ids))

        return filters

    async def get_skills_count(
        self,
        session: AsyncSession,
        query: str | Type[Empty] = Empty,
        skill_ids: list[uuid.UUID] | Type[Empty] = Empty,
        exclude_skill_ids: list[uuid.UUID] | Type[Empty] = Empty,
    ) -> int:
        statement = select(func.count(Skill.id)) # pylint: disable=not-callable

        filters = await self._get_skills_filters(
            query=query,
            skill_ids=skill_ids,
            exclude_skill_ids=exclude_skill_ids,
        )

        statement = statement.where(*filters)
        result = await session.scalar(statement)

        return result

    async def get_skills(
        self,
        session: AsyncSession,
        query: str | Type[Empty] = Empty,
        skill_ids: list[uuid.UUID] | Type[Empty] = Empty,
        exclude_skill_ids: list[uuid.UUID] | Type[Empty] = Empty,
        page: int = 1,
        per_page: int = 10,
    ) -> list[Skill]:
        statement = select(Skill).order_by(desc(Skill.created_at))

        filters = await self._get_skills_filters(
            query=query,
            skill_ids=skill_ids,
            exclude_skill_ids=exclude_skill_ids,
        )

        statement = statement.where(*filters)

        offset = (page - 1) * per_page
        statement = statement.limit(per_page).offset(offset)

        skills = await session.execute(statement)

        return list(skills.unique().scalars().all())

    async def get_skill(self, session: AsyncSession, habr_id: int) -> Skill | None:
        query = select(Skill).where(Skill.habr_id == habr_id)

        result = await session.execute(query)

        return result.unique().scalar_one_or_none()


def get_service(settings: Settings) -> Service:
    return Service(dsn=str(settings.dsn))

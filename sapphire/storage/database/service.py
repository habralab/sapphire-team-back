import pathlib
from typing import Type

from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from sapphire.common.database.service import BaseDatabaseService
from sapphire.common.utils.empty import Empty
from sapphire.storage.database.models import (
    Base,
    Skill,
    Specialization,
    SpecializationGroup,
    SpecializationsSkills,
)
from sapphire.storage.settings import StorageSettings


class StorageDatabaseService(BaseDatabaseService):
    def get_alembic_config_path(self) -> pathlib.Path:
        return pathlib.Path(__file__).parent / "migrations"

    def get_fixtures_directory_path(self) -> pathlib.Path | None:
        return pathlib.Path(__file__).parent / "fixtures"

    def get_models(self) -> list[Type[Base]]:
        return [Skill, Specialization, SpecializationGroup, SpecializationsSkills]

    async def get_specializations(
        self,
        session: AsyncSession,
        page: int | Type[Empty] = Empty,
        per_page: int | Type[Empty] = Empty,
    ) -> list[Specialization]:
        query = select(Specialization).order_by(desc(Specialization.created_at))

        if page is not None and per_page is not None:
            offset = (page - 1) * per_page
            query = query.limit(per_page).offset(offset)

        specializations = await session.execute(query)

        return list(specializations.scalars().all())

    async def get_specialization_groups(
        self,
        session: AsyncSession,
        query_text: str | Type[Empty] = Empty,
        page: int | Type[Empty] = Empty,
        per_page: int | Type[Empty] = Empty,
    ) -> list[SpecializationGroup]:
        query = select(SpecializationGroup).order_by(desc(SpecializationGroup.created_at))

        filters = []
        if query_text is not Empty:
            filters.append(SpecializationGroup.name.contains(query_text))

        query = query.where(*filters)

        if page is not Empty and per_page is not Empty:
            offset = (page - 1) * per_page
            query = query.limit(per_page).offset(offset)

        specialization_groups = await session.execute(query)

        return list(specialization_groups.scalars().all())

    async def get_skills(
        self,
        session: AsyncSession,
        query_text: str | Type[Empty] = Empty,
        page: int | Type[Empty] = Empty,
        per_page: int | Type[Empty] = Empty,
    ) -> list[Skill]:
        query = select(Skill).order_by(desc(Skill.created_at))

        filters = []
        if query_text is not Empty:
            filters.append(Skill.name.contains(query_text))

        query = query.where(*filters)
        skills = await session.execute(query)

        if page is not Empty and per_page is not Empty:
            offset = (page - 1) * per_page
            query = query.limit(per_page).offset(offset)

        return list(skills.scalars().all())


def get_service(settings: StorageSettings) -> StorageDatabaseService:
    return StorageDatabaseService(dsn=str(settings.db_dsn))

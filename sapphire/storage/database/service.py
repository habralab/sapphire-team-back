import pathlib
from typing import List

from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from sapphire.common.database.service import BaseDatabaseService
from sapphire.storage.database.models import Specialization
from sapphire.storage.settings import StorageSettings


class StorageDatabaseService(BaseDatabaseService):
    def get_alembic_config_path(self) -> pathlib.Path:
        return pathlib.Path(__file__).parent / "migrations"

    async def get_specializations_paginated(
        self,
        session: AsyncSession,
        page: int,
        per_page: int,
    ) -> List[Specialization]:

        offset = (page - 1) * per_page

        specializations_pagged = await session.execute(
            (
                select(Specialization)
                .order_by(desc(Specialization.created_at))
                .limit(per_page)
                .offset(offset)
            )
        )

        return [spec._asdict()["Specialization"] for spec in specializations_pagged]


def get_service(settings: StorageSettings) -> StorageDatabaseService:
    return StorageDatabaseService(dsn=str(settings.db_dsn))

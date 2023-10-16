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

    async def get_specializations(
        self,
        session: AsyncSession,
        page: int | None,
        per_page: int | None,
    ) -> List[Specialization]:

        query = (
            select(Specialization)
            .order_by(desc(Specialization.created_at))
            )

        if page is not None and per_page is not None:
            offset = (page - 1) * per_page
            query = (
                query
                .limit(per_page)
                .offset(offset)
            )

        specializations = await session.execute(query)

        return [spec._asdict()["Specialization"] for spec in specializations]


def get_service(settings: StorageSettings) -> StorageDatabaseService:
    return StorageDatabaseService(dsn=str(settings.db_dsn))

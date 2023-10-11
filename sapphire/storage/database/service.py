import pathlib

from sqlalchemy.ext.asyncio import AsyncSession

from sapphire.common.database.service import BaseDatabaseService
from sapphire.storage.settings import StorageSettings


class StorageDatabaseService(BaseDatabaseService):
    def get_alembic_config_path(self) -> pathlib.Path:
        return pathlib.Path(__file__).parent / "migrations"

    async def get_specializations_paginated(
        self,
        session: AsyncSession,
        page_number: int,
        per_page: int,
    ):
        specializations = await session.query(
            Specialization
                ).filter(Specialization.migrate_to == None
                    ).order_by(
                        Specialization.created_at.desc()
                    )

        paginated_specializations = specializations.paginate(page, per_page, error_out=False)

        return paginated_specializations


def get_service(settings: StorageSettings) -> StorageDatabaseService:
    return StorageDatabaseService(dsn=str(settings.db_dsn))

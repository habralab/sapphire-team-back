import pathlib

from alembic import command as alembic_command
from alembic.config import Config as AlembicConfig
from facet import ServiceMixin
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine


class BaseDatabaseService(ServiceMixin):
    def __init__(self, dsn: str):
        self._dsn = dsn
        self._engine = create_async_engine(self._dsn)
        self._sessionmaker = async_sessionmaker(self._engine, expire_on_commit=False)

    def base_get_alembic_config_path(self) -> pathlib.Path:
        raise NotImplementedError

    def base_get_alembic_config(self) -> AlembicConfig:
        migrations_path = self.base_get_alembic_config_path()
        
        config = AlembicConfig()
        config.set_main_option("script_location", str(migrations_path))
        config.set_main_option("sqlalchemy.url", self._dsn)

        return config

    def bae_migrate(self):
        alembic_command.upgrade(self.base_get_alembic_config(), "head")

    def base_create_migration(self, message: str | None = None):
        alembic_command.revision(self.base_get_alembic_config(), message=message, autogenerate=True)

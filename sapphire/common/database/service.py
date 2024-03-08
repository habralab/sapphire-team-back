import enum
import json
import pathlib
import uuid
from contextlib import asynccontextmanager
from typing import Any, Iterable, Type

import yaml
from alembic import command as alembic_command
from alembic.config import Config as AlembicConfig
from facet import ServiceMixin
from loguru import logger
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase


class FixtureFormatEnum(str, enum.Enum):
    YAML = "yaml"
    JSON = "json"


class FixtureMetadata(BaseModel):
    name: str
    format: FixtureFormatEnum


class FixtureContent(BaseModel):
    model: str
    data: list[dict[str, Any]]


class BaseDatabaseService(ServiceMixin):
    FIXTURES_FORMATS_MAPPING = {
        FixtureFormatEnum.YAML: lambda filepath: list(yaml.safe_load_all(filepath)),
        FixtureFormatEnum.JSON: json.load,
    }

    def __init__(self, dsn: str):
        self._dsn = dsn
        self._engine = create_async_engine(self._dsn, pool_recycle=60)
        self._sessionmaker = async_sessionmaker(self._engine, expire_on_commit=False)

    def get_migrations_directory_path(self) -> pathlib.Path:
        raise NotImplementedError(
            "For working with migrations you need override `get_migrations_directory_path` method",
        )

    def get_alembic_config(self) -> AlembicConfig:
        migrations_path = self.get_migrations_directory_path()

        config = AlembicConfig()
        config.set_main_option("script_location", str(migrations_path))
        config.set_main_option("sqlalchemy.url", self._dsn.replace("%", "%%"))

        return config

    def get_fixtures_directory_path(self) -> pathlib.Path:
        raise NotImplementedError(
            "For working with fixtures you need override `get_fixtures_directory_path` method",
        )

    def get_models(self) -> Iterable[Type[DeclarativeBase]]:
        raise NotImplementedError(
            "For working with fixtures you need override `get_models_mapping` method",
        )

    def prepare_fixture_fields_for_model(self, fields: dict[str, Any]) -> dict[str, Any]:
        for name, value in fields.items():
            if isinstance(value, str):
                try:
                    fields[name] = uuid.UUID(value)
                except ValueError:
                    pass

        return fields

    @asynccontextmanager
    async def transaction(self):
        async with self._sessionmaker() as session:
            async with session.begin():
                yield session

    def migrate(self):
        alembic_command.upgrade(self.get_alembic_config(), "head")

    def rollback(self, revision: str | None = None):
        revision = revision or "-1"

        alembic_command.downgrade(self.get_alembic_config(), revision)

    def show_migrations(self):
        alembic_command.history(self.get_alembic_config())

    def create_migration(self, message: str | None = None):
        alembic_command.revision(
            self.get_alembic_config(), message=message, autogenerate=True,
        )

    def get_fixtures(self) -> list[FixtureMetadata]:
        fixtures_directory_path = self.get_fixtures_directory_path()
        extension_values = set(FixtureFormatEnum)
        fixtures_data = []

        for element in fixtures_directory_path.glob("*"):
            if not element.is_file():
                continue
            extension = element.suffix.lstrip(".")
            if extension not in extension_values:
                continue
            fixture_data = FixtureMetadata(name=element.stem, format=FixtureFormatEnum(extension))
            fixtures_data.append(fixture_data)

        return fixtures_data

    async def apply_fixture(
            self,
            name: str,
            fixture_format: FixtureFormatEnum = FixtureFormatEnum.YAML,
    ):
        fixtures_directory_path = self.get_fixtures_directory_path()

        fixture_file_path = fixtures_directory_path / f"{name}.{fixture_format.value}"
        fixture_file_loader = self.FIXTURES_FORMATS_MAPPING[fixture_format]
        with open(fixture_file_path, "rt", encoding="utf-8") as fixture_file:
            fixture_payload = fixture_file_loader(fixture_file)
        logger.info("Load fixture '{}'", name)

        if isinstance(fixture_payload, dict):
            fixture_payload = [fixture_payload]
        elif not isinstance(fixture_payload, list):
            raise ValueError(f"Fixture '{name}' have incorrect format: must be dict or list")
        async with self.transaction() as session:
            for payload in fixture_payload:
                await self._apply_fixture(name=name, payload=payload, session=session)
        logger.info("Fixture '{}' apply to database", name)

    async def _apply_fixture(self, name: str, payload: dict[str, Any], session: AsyncSession):
        content = FixtureContent(**payload)
        models_mapping = {model.__tablename__: model for model in self.get_models()}
        model = models_mapping.get(content.model)
        if model is None:
            raise ValueError(f"Incorrect model name in fixture '{name}': {content.model}")

        records = [
            model(**self.prepare_fixture_fields_for_model(fields))
            for fields in content.data
        ]
        session.add_all(records)

    async def start(self):
        logger.info("Start Database service")

    async def stop(self):
        logger.info("Stop Database service")

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from sapphire.common.database.service import BaseDatabaseService


@pytest.mark.skip("Implement in future")
@pytest.mark.asyncio
async def test_transaction(database_service: BaseDatabaseService):
    sessionmaker_mock = AsyncMock() 

    with patch.object(database_service, "_sessionmaker", sessionmaker_mock):
        async with database_service.transaction():
            sessionmaker_mock.assert_called_once_with()


@patch("sapphire.common.database.service.alembic_command")
def test_create_migration(mock_alembic_command: MagicMock, database_service: BaseDatabaseService):
    message = "Any message"
    config = MagicMock()

    with patch.object(
            database_service,
            "get_alembic_config",
            return_value=config,
    ) as get_alembic_config_mock:
        database_service.create_migration(message=message)

    get_alembic_config_mock.assert_called_once()
    mock_alembic_command.revision.assert_called_once_with(
        config,
        message=message,
        autogenerate=True,
    )


@patch("sapphire.common.database.service.alembic_command")
def test_migrate(mock_alembic_command: MagicMock, database_service: BaseDatabaseService):
    config = MagicMock()

    with patch.object(
            database_service,
            "get_alembic_config",
            return_value=config,
    ) as get_alembic_config_mock:
        database_service.migrate()

    get_alembic_config_mock.assert_called_once()
    mock_alembic_command.upgrade.assert_called_once_with(config, "head")

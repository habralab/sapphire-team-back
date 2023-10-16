import uuid
from unittest.mock import AsyncMock, MagicMock

import pytest

from sapphire.storage.database.models import Specialization
from sapphire.storage.database.service import StorageDatabaseService


@pytest.mark.asyncio
async def test_get_specializations_paginated(database_service:StorageDatabaseService):
    ...

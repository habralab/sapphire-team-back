import uuid
from unittest.mock import AsyncMock, MagicMock

import pytest

from sapphire.storage.database.models import Specialization
from sapphire.storage.database.service import StorageDatabaseService


@pytest.mark.asyncio
async def test_get_specializations_paginated(database_service:StorageDatabaseService):
    session = MagicMock()

    specialization1 = Specialization(id=uuid.uuid4())
    specialization2 = Specialization(id=uuid.uuid4())

    mock_specializations = MagicMock(return_value=[specialization1, specialization2])

    session.return_value.execute.return_value.paginate.return_value = mock_specializations

    paginated_specializations = await database_service.get_specializations_paginated(
        session=session, page=1, per_page=1
        )

    assert mock_specializations == paginated_specializations

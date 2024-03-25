import uuid
from typing import Type

import pytest

from autotests.clients.rest.storage.client import StorageRestClient
from autotests.utils import Empty


@pytest.mark.parametrize(
    ("query", "group_id", "specialization_ids", "exclude_specialization_ids"),
    (
        (Empty, Empty, Empty, Empty),
        ("Developer", uuid.uuid4(), [uuid.uuid4()], [uuid.uuid4()]),
    ),
)
@pytest.mark.asyncio
async def test_specializations(
        storage_rest_client: StorageRestClient,
        query: str | Type[Empty],
        group_id: uuid.UUID | Type[Empty],
        specialization_ids: list[uuid.UUID] | Type[Empty],
        exclude_specialization_ids: list[uuid.UUID] | Type[Empty],
):
    await storage_rest_client.get_specializations(
        query=query,
        group_id=group_id,
        specialization_ids=specialization_ids,
        exclude_specialization_ids=exclude_specialization_ids,
    )

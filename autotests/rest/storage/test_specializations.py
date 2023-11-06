import uuid
from typing import Type

import pytest

from autotests.clients.rest.storage.client import StorageRestClient
from autotests.utils import Empty


@pytest.mark.parametrize(
    ("query_text", "is_other", "group_id",),
    (
        (Empty, Empty, Empty),
        ("Developer", True, uuid.uuid4()),
    )
)
@pytest.mark.asyncio
async def test_specializations(
        storage_rest_client: StorageRestClient,
        query_text: str | Type[Empty],
        is_other: bool | Type[Empty],
        group_id: uuid.UUID | Type[Empty],
):
    await storage_rest_client.get_specializations(
        query_text=query_text,
        is_other=is_other,
        group_id=group_id
    )

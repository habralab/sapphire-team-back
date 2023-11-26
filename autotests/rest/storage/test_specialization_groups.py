import uuid
from typing import Type

import pytest

from autotests.clients.rest.storage.client import StorageRestClient
from autotests.utils import Empty


@pytest.mark.parametrize(("query_text", "group_ids", "exclude_group_ids"), (
    (Empty, Empty, Empty),
    ("Developer", [uuid.uuid4()], [uuid.uuid4()]),
))
@pytest.mark.asyncio
async def test_get_specialization_groups(
        storage_rest_client: StorageRestClient,
        query_text: str | Type[Empty],
        group_ids: list[uuid.UUID] | Type[Empty],
        exclude_group_ids: list[uuid.UUID] | Type[Empty],
):
    await storage_rest_client.get_specialization_groups(
        query_text=query_text,
        group_ids=group_ids,
        exclude_group_ids=exclude_group_ids,
    )

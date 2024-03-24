import uuid
from typing import Type

import pytest

from autotests.clients.rest.storage.client import StorageRestClient
from autotests.utils import Empty


@pytest.mark.parametrize(("query", "skill_ids", "exclude_skill_ids"), (
    (Empty, Empty, Empty),
    ("Python", Empty, [uuid.uuid4(), uuid.uuid4()]),
    (Empty, [uuid.uuid4(), uuid.uuid4()], Empty),
))
@pytest.mark.asyncio
async def test_get_skills(
        storage_rest_client: StorageRestClient,
        query: str | Type[Empty],
        skill_ids: list[uuid.UUID] | Type[Empty],
        exclude_skill_ids: list[uuid.UUID] | Type[Empty],
):
    await storage_rest_client.get_skills(
        query=query,
        skill_ids=skill_ids,
        exclude_skill_ids=exclude_skill_ids,
    )

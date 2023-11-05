from typing import Type

import pytest

from autotests.clients.rest.storage.client import StorageRestClient
from autotests.utils import Empty


@pytest.mark.parametrize("query_text", (Empty, "Python"))
@pytest.mark.asyncio
async def test_get_skills(storage_rest_client: StorageRestClient, query_text: str | Type[Empty]):
    await storage_rest_client.get_skills(query_text=query_text)

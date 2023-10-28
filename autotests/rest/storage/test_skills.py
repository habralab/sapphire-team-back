import pytest

from autotests.clients.rest.storage.client import StorageRestClient


@pytest.mark.asyncio
async def test_get_skills(storage_rest_client: StorageRestClient):
    await storage_rest_client.get_skills()

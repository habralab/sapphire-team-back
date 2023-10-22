import pytest

from .client import StorageRestClient


@pytest.mark.asyncio
async def test_health(storage_rest_client: StorageRestClient):
    await storage_rest_client.get_health()

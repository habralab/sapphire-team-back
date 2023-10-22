import pytest

from .client import UsersRestClient


@pytest.mark.asyncio
async def test_health(users_rest_client: UsersRestClient):
    await users_rest_client.get_health()

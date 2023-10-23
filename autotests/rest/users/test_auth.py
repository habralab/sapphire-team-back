import pytest

from autotests.rest.users.client.client import UsersRestClient


@pytest.mark.asyncio
async def test_logout(oleg_users_rest_client: UsersRestClient):
    await oleg_users_rest_client.logout()

import uuid

import pytest
import yarl

from autotests.clients.rest.users.client import UsersRestClient
from autotests.settings import AutotestsSettings


@pytest.mark.asyncio
async def test_oauth2_habr_authorize_redirect(
        settings: AutotestsSettings,
        users_rest_client: UsersRestClient,
):
    response = await users_rest_client.oauth2_habr_authorize()
    location = response.headers.get("Location")
    assert location
    location_url = yarl.URL(location)

    assert location_url.host == "account.habr.com"
    assert location_url.path == "/oauth/authorize/"
    assert set(location_url.query.keys()) == {"client_id", "state", "redirect_uri", "response_type"}
    assert location_url.query["redirect_uri"] == str(settings.habr_oauth2_callback_url)
    assert location_url.query["response_type"] == "code"


@pytest.mark.asyncio
async def test_logout(oleg_users_rest_client: UsersRestClient):
    await oleg_users_rest_client.logout()


@pytest.mark.parametrize(("client", "user_id", "is_activated"), (
    (
        pytest.lazy_fixture("oleg_users_rest_client"),
        pytest.lazy_fixture("oleg_id"),
        False,
    ),
    (
        pytest.lazy_fixture("matvey_users_rest_client"),
        pytest.lazy_fixture("matvey_id"),
        False,
    ),
    (
        pytest.lazy_fixture("oleg_activated_users_rest_client"),
        pytest.lazy_fixture("oleg_id"),
        True,
    ),
    (
        pytest.lazy_fixture("matvey_activated_users_rest_client"),
        pytest.lazy_fixture("matvey_id"),
        True,
    ),
))
@pytest.mark.asyncio
async def test_check(client: UsersRestClient, user_id: uuid.UUID, is_activated: bool):
    jwt_data = await client.check_auth()

    assert jwt_data.user_id == user_id
    assert jwt_data.is_activated == is_activated

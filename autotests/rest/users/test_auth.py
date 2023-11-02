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


@pytest.mark.parametrize(("client", "expected_is_auth"), (
    (pytest.lazy_fixture("users_rest_client"), False),
    (pytest.lazy_fixture("oleg_users_rest_client"), True),
    (pytest.lazy_fixture("matvey_users_rest_client"), True),
))
@pytest.mark.asyncio
async def test_check(client: UsersRestClient, expected_is_auth: bool):
    is_auth = await client.check_auth()

    assert is_auth is expected_is_auth

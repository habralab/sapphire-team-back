import pytest
import yarl

from autotests.rest.users.client.client import UsersRestClient
from autotests.settings import AutotestsSettings


@pytest.mark.asyncio
async def test_oauth2_habr_authorize_redirect(
        settings: AutotestsSettings,
        users_rest_client: UsersRestClient,
):
    expected_redirect_uri = (
        yarl.URL(str(settings.users_base_url)) / "api" / "v1beta" / "rest" / "auth" / "oauth2" /
        "habr" / "callback"
    )

    response = await users_rest_client.oauth2_habr_authorize()

    location = response.headers.get("Location")
    assert location

    location_url = yarl.URL(location)

    assert location_url.host == "account.habr.com"
    assert location_url.path == "/oauth/authorize/"
    assert set(location_url.query.keys()) == {"client_id", "state", "redirect_uri", "response_type"}
    assert location_url.query["redirect_uri"] == str(expected_redirect_uri)
    assert location_url.query["response_type"] == "code"


@pytest.mark.asyncio
async def test_logout(oleg_users_rest_client: UsersRestClient):
    await oleg_users_rest_client.logout()

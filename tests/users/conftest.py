import pytest

from sapphire.users.settings import UsersSettings


@pytest.fixture()
def settings() -> UsersSettings:
    return UsersSettings(
        habr_oauth2_client_id="habr_oauth2_client_id",
        habr_oauth2_client_secret="habr_oauth2_client_secret",
    )

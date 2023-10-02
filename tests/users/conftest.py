import pytest

from sapphire.users.settings import UsersSettings


@pytest.fixture()
def settings() -> UsersSettings:
    return UsersSettings()

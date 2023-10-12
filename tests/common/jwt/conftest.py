import pytest

from sapphire.common.jwt import JWTMethods, get_jwt_methods
from sapphire.common.jwt.settings import JWTSettings


@pytest.fixture()
def settings() -> JWTSettings:
    return JWTSettings()


@pytest.fixture()
def jwt_methods(settings: JWTSettings) -> JWTMethods:
    return get_jwt_methods(settings=settings)

import pytest

from collabry.common.jwt import JWTMethods, get_jwt_methods
from collabry.common.jwt.settings import JWTSettings


@pytest.fixture()
def settings() -> JWTSettings:
    return JWTSettings()


@pytest.fixture()
def jwt_methods(settings: JWTSettings) -> JWTMethods:
    return get_jwt_methods(settings=settings)

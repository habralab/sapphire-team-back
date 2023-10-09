from unittest.mock import Mock

import pytest

from sapphire.common.jwt import JWTMethods, get_jwt_methods
from sapphire.common.jwt.settings import JWTSettings


@pytest.fixture()
def settings() -> JWTSettings:
    return JWTSettings()


@pytest.fixture()
def jwt_methods(settings: JWTSettings) -> JWTMethods:
    return get_jwt_methods(settings=settings)


@pytest.fixture()
def mocked_request(jwt_methods: JWTMethods) -> Mock:
    request = Mock()
    request.app.service.jwt_methods = jwt_methods
    request.cookies = {}
    return request


@pytest.fixture()
def mocked_response() -> Mock:
    response = Mock()
    response.set_cookie = Mock(name="set_cookie")
    return response

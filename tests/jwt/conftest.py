from unittest.mock import Mock

import pytest

from sapphire.common.api.jwt import JWTMethods, get_jwt_methods
from sapphire.common.api.jwt.settings import JWTSettings, get_settings


@pytest.fixture()
def settings():
    return get_settings()


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

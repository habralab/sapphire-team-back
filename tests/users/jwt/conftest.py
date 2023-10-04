from unittest.mock import Mock

import pytest

from sapphire.users.jwt import JWTMethods, get_jwt_methods
from sapphire.users.settings import UsersSettings


@pytest.fixture()
def jwt_methods(settings: UsersSettings) -> JWTMethods:
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

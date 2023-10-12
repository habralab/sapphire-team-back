from unittest.mock import Mock

import pytest

from sapphire.common.jwt.methods import JWTMethods


@pytest.fixture()
def mocked_request(jwt_methods: JWTMethods) -> Mock:
    request = Mock()
    request.app.service.jwt_methods = jwt_methods
    request.cookies = {}
    return request


@pytest.fixture()
def mocked_response() -> Mock:
    response = Mock()
    response.set_cookie = Mock()
    return response

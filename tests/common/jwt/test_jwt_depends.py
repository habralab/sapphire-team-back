import uuid

import fastapi
import pytest

from sapphire.common.api.jwt import JWTMethods
from sapphire.common.api.jwt.depends import get_user_id


def test_get_user_id(jwt_methods: JWTMethods, mocked_request, mocked_response):
    # Check priority from tokens
    user_id_1 = uuid.uuid4()
    user_id_2 = uuid.uuid4()
    access_token = jwt_methods.issue_access_token(user_id_1)
    refresh_token = jwt_methods.issue_refresh_token(user_id_2)
    mocked_request.cookies.update(
        {"access_token": access_token, "refresh_token": refresh_token}
    )
    parsed_user_id = get_user_id(mocked_response, mocked_request)
    assert parsed_user_id == user_id_1


def test_parse_user_id_without_access_token(
    jwt_methods: JWTMethods, mocked_request, mocked_response
):
    user_id = uuid.uuid4()
    refresh_token = jwt_methods.issue_refresh_token(user_id)
    mocked_request.cookies.update({"refresh_token": refresh_token})
    parsed_user_id = get_user_id(mocked_response, mocked_request)
    assert parsed_user_id == user_id


def test_parse_user_id_without_tokens(mocked_request, mocked_response):
    with pytest.raises(fastapi.HTTPException) as excinfo:
        get_user_id(mocked_response, mocked_request)
    assert excinfo.value.status_code == 401

import uuid
from unittest.mock import Mock

import fastapi
import pytest

from sapphire.common.jwt import JWTMethods
from sapphire.common.jwt.dependencies.rest import get_user_id


def test_get_user_id_from_access_cookie(
        jwt_methods: JWTMethods,
        mocked_request: Mock,
        mocked_response: Mock,
):
    # Check priority from tokens
    user_id_1 = uuid.uuid4()
    user_id_2 = uuid.uuid4()
    access_token = jwt_methods.issue_access_token(user_id_1)
    refresh_token = jwt_methods.issue_refresh_token(user_id_2)
    
    parsed_user_id = get_user_id(
        response=mocked_response,
        request=mocked_request,
        access_token_from_cookie=access_token,
        refresh_token_from_cookie=refresh_token,
        access_token_from_header=None,
    )
    
    assert parsed_user_id == user_id_1


def test_get_user_id_from_refresh_cookie(
    jwt_methods: JWTMethods, mocked_request: Mock, mocked_response: Mock,
):
    user_id = uuid.uuid4()
    refresh_token = jwt_methods.issue_refresh_token(user_id)

    parsed_user_id = get_user_id(
        response=mocked_response,
        request=mocked_request,
        access_token_from_cookie=None,
        refresh_token_from_cookie=refresh_token,
        access_token_from_header=None,
    )

    assert parsed_user_id == user_id


def test_parse_user_id_without_tokens(mocked_request: Mock, mocked_response: Mock):
    with pytest.raises(fastapi.HTTPException) as excinfo:
        get_user_id(
            response=mocked_response,
            request=mocked_request,
            access_token_from_cookie=None,
            refresh_token_from_cookie=None,
            access_token_from_header=None,
        )
    assert excinfo.value.status_code == 401

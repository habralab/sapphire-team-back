import uuid
from unittest.mock import Mock

import pytest

from sapphire.common.jwt import JWTMethods
from sapphire.common.jwt.dependencies.rest import get_jwt_data


@pytest.mark.asyncio
async def test_get_request_user_id_from_access_cookie(
        jwt_methods: JWTMethods,
        mocked_request: Mock,
        mocked_response: Mock,
):
    # Check priority from tokens
    user_id_1 = uuid.uuid4()
    is_activated_1 = True
    user_id_2 = uuid.uuid4()
    is_activated_2 = False
    access_token = jwt_methods.issue_access_token(user_id=user_id_1, is_activated=is_activated_1)
    refresh_token = jwt_methods.issue_refresh_token(user_id=user_id_2, is_activated=is_activated_2)
    
    jwt_data = await get_jwt_data(
        response=mocked_response,
        request=mocked_request,
        access_token_from_cookie=access_token,
        refresh_token_from_cookie=refresh_token,
        access_token_from_header=None,
    )
    
    assert jwt_data is not None
    assert jwt_data.user_id == user_id_1
    assert jwt_data.is_activated == is_activated_1


@pytest.mark.asyncio
async def test_get_request_user_id_from_refresh_cookie(
    jwt_methods: JWTMethods, mocked_request: Mock, mocked_response: Mock,
):
    user_id = uuid.uuid4()
    is_activated = True
    refresh_token = jwt_methods.issue_refresh_token(user_id=user_id, is_activated=is_activated)

    jwt_data = await get_jwt_data(
        response=mocked_response,
        request=mocked_request,
        access_token_from_cookie=None,
        refresh_token_from_cookie=refresh_token,
        access_token_from_header=None,
    )

    assert jwt_data is not None
    assert jwt_data.user_id == user_id
    assert jwt_data.is_activated == is_activated


@pytest.mark.asyncio
async def test_get_request_user_id_without_tokens(mocked_request: Mock, mocked_response: Mock):
    jwt_data = await get_jwt_data(
        response=mocked_response,
        request=mocked_request,
        access_token_from_cookie=None,
        refresh_token_from_cookie=None,
        access_token_from_header=None,
    )

    assert jwt_data is None

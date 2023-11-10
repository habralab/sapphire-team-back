import uuid

import jwt

from sapphire.common.jwt import JWTMethods
from sapphire.common.jwt.settings import JWTSettings


def test_correct_access_token(jwt_methods: JWTMethods):
    user_id = uuid.uuid4()
    is_activated = True
    access_token = jwt_methods.issue_access_token(user_id=user_id, is_activated=is_activated)
    jwt_data = jwt_methods.decode_access_token(access_token)
    
    assert jwt_data is not None
    assert jwt_data.user_id == user_id
    assert jwt_data.is_activated == is_activated


def test_fake_access_token(jwt_methods: JWTMethods):
    fake_access_token = "access_token"
    jwt_data = jwt_methods.decode_access_token(fake_access_token)
    assert jwt_data is None


def test_not_user_id_access_token(settings: JWTSettings, jwt_methods: JWTMethods):
    fake_access_token = jwt.encode(
        {"something": "like this"},
        settings.jwt_access_token_private_key,
        algorithm="RS256",
    )
    jwt_data = jwt_methods.decode_access_token(fake_access_token)
    assert jwt_data is None


def test_correct_refresh_token(jwt_methods: JWTMethods):
    user_id = uuid.uuid4()
    is_activated = False
    refresh_token = jwt_methods.issue_refresh_token(user_id=user_id, is_activated=is_activated)
    jwt_data = jwt_methods.decode_refresh_token(refresh_token)

    assert jwt_data is not None
    assert jwt_data.user_id == user_id
    assert jwt_data.is_activated == is_activated


def test_fake_refresh_token(jwt_methods: JWTMethods):
    fake_refresh_token = "access_token"
    jwt_data = jwt_methods.decode_refresh_token(fake_refresh_token)
    assert jwt_data is None


def test_not_user_id_refresh_token(settings: JWTSettings, jwt_methods: JWTMethods):
    fake_refresh_token = jwt.encode(
        {"something": "like this"},
        settings.jwt_access_token_private_key,
        algorithm="RS256",
    )
    jwt_data = jwt_methods.decode_refresh_token(fake_refresh_token)
    assert jwt_data is None

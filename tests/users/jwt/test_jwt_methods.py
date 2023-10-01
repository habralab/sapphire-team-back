import jwt

from sapphire.users.jwt import JWTMethods
from sapphire.users.settings import UsersSettings


def test_correct_access_token(jwt_methods: JWTMethods):
    user_id = 123
    access_token = jwt_methods.issue_access_token(user_id)
    decoded_user_id = jwt_methods.decode_access_token(access_token)
    assert decoded_user_id == user_id


def test_fake_access_token(jwt_methods: JWTMethods):
    fake_access_token = "access_token"
    decoded_user_id = jwt_methods.decode_access_token(fake_access_token)
    assert decoded_user_id is None


def test_not_user_id_access_token(settings: UsersSettings, jwt_methods: JWTMethods):
    fake_access_token = jwt.encode(
        {"something": "like this"},
        settings.jwt_access_token_private_key,
        algorithm="RS256",
    )
    decoded_user_id = jwt_methods.decode_access_token(fake_access_token)
    assert decoded_user_id is None


def test_correct_refresh_token(jwt_methods: JWTMethods):
    user_id = 123
    refresh_token = jwt_methods.issue_refresh_token(user_id)
    decoded_user_id = jwt_methods.decode_refresh_token(refresh_token)
    assert decoded_user_id == user_id


def test_fake_refresh_token(jwt_methods: JWTMethods):
    fake_refresh_token = "access_token"
    decoded_user_id = jwt_methods.decode_refresh_token(fake_refresh_token)
    assert decoded_user_id is None


def test_not_user_id_refresh_token(settings: UsersSettings, jwt_methods: JWTMethods):
    fake_refresh_token = jwt.encode(
        {"something": "like this"},
        settings.jwt_access_token_private_key,
        algorithm="RS256",
    )
    decoded_user_id = jwt_methods.decode_access_token(fake_refresh_token)
    assert decoded_user_id is None

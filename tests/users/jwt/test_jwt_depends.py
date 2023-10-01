import fastapi

from sapphire.users.jwt import JWTMethods
from sapphire.users.jwt.depends import parse_user_id, verify_jwt_tokens


def test_parse_user_id(jwt_methods: JWTMethods, mocked_request):
    # Check priority from tokens
    user_id_1 = 1
    user_id_2 = 2
    access_token = jwt_methods.issue_access_token(user_id_1)
    refresh_token = jwt_methods.issue_refresh_token(user_id_2)
    mocked_request.cookies.update(
        {"access_token": access_token, "refresh_token": refresh_token}
    )
    parsed_user_id = parse_user_id(mocked_request)
    assert parsed_user_id == user_id_1


def test_parse_user_id_without_access_token(jwt_methods: JWTMethods, mocked_request):
    user_id = 123
    refresh_token = jwt_methods.issue_refresh_token(user_id)
    mocked_request.cookies.update({"refresh_token": refresh_token})
    parsed_user_id = parse_user_id(mocked_request)
    assert parsed_user_id == user_id


def test_parse_user_id_without_tokens(mocked_request):
    parsed_user_id = parse_user_id(mocked_request)
    assert parsed_user_id is None


def test_verify_jwt_tokens(mocked_request, mocked_response, jwt_methods: JWTMethods):
    user_id = 1
    access_token = jwt_methods.issue_access_token(user_id)
    refresh_token = jwt_methods.issue_refresh_token(user_id)
    mocked_request.cookies.update(
        {"access_token": access_token, "refresh_token": refresh_token}
    )
    verify_result = verify_jwt_tokens(mocked_response, mocked_request)
    assert verify_result is None


def test_verify_jwt_tokens_without_access_token(
    mocked_request, mocked_response, jwt_methods: JWTMethods
):
    user_id = 1
    refresh_token = jwt_methods.issue_refresh_token(user_id)
    mocked_request.cookies.update({"refresh_token": refresh_token})
    verify_result = verify_jwt_tokens(mocked_response, mocked_request)
    assert verify_result is None


def test_verify_jwt_tokens_without_tokens(mocked_request, mocked_response):
    received_http_exception = False
    try:
        verify_jwt_tokens(mocked_response, mocked_request)
    except fastapi.HTTPException:
        received_http_exception = True
    finally:
        assert received_http_exception, "Expected fastapi.HTTPException"

import fastapi

from .base import JWTMethods


def verify_jwt_tokens(response: fastapi.Response, request: fastapi.Request):
    access_token = request.cookies.get("access_token", None)
    refresh_token = request.cookies.get("refresh_token", None)
    jwt_methods: JWTMethods = request.app.service.jwt_methods

    if access_token is None:
        if refresh_token is None:
            raise fastapi.HTTPException(status_code=403, detail="Missing tokens")
        refresh_token_user_id = jwt_methods.decode_refresh_token(refresh_token)
        if refresh_token_user_id is None:
            raise fastapi.HTTPException(status_code=403, detail="Access denied")
        # Update access token
        new_access_token = jwt_methods.issue_access_token(refresh_token_user_id)
        response.set_cookie(
            key="access_token",
            value=new_access_token,
            expires=int(jwt_methods.access_token_expires.total_seconds()),
            path="/",
            secure=True,
            httponly=True,
            samesite="none",
        )
    else:
        access_token_user_id = jwt_methods.decode_access_token(access_token)
        if access_token_user_id is None:
            raise fastapi.HTTPException(status_code=403, detail="Access denied")
    # verify is ok


def parse_user_id(request: fastapi.Request):
    jwt_methods: JWTMethods = request.app.service.jwt_methods
    access_token = request.cookies.get("access_token")
    refresh_token = request.cookies.get("refresh_token")
    access_token_user_id = jwt_methods.decode_access_token(access_token)
    refresh_token_user_id = jwt_methods.decode_refresh_token(refresh_token)
    return access_token_user_id or refresh_token_user_id

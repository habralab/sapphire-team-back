import uuid

import fastapi

from .methods import JWTMethods


def get_user_id(response: fastapi.Response, request: fastapi.Request) -> uuid.UUID:
    # Verify JWT tokens
    access_token = request.cookies.get("access_token", None)
    refresh_token = request.cookies.get("refresh_token", None)
    jwt_methods: JWTMethods = request.app.service.jwt_methods

    if access_token is None:
        if refresh_token is None:
            raise fastapi.HTTPException(status_code=401, detail="Not authenticated")
        refresh_token_user_id = jwt_methods.decode_refresh_token(refresh_token)
        if refresh_token_user_id is None:
            raise fastapi.HTTPException(status_code=401, detail="Not authenticated")
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
        return refresh_token_user_id
    access_token_user_id = jwt_methods.decode_access_token(access_token)
    if access_token_user_id is None:
        raise fastapi.HTTPException(status_code=401, detail="Not authenticated")
    return access_token_user_id

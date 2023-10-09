import uuid

import fastapi

from sapphire.common.api.exceptions import HTTPNotAuthenticated
from sapphire.common.jwt.methods import JWTMethods


def get_user_id(
        websocket: fastapi.WebSocket,
        access_token_from_cookie: str | None = fastapi.Cookie(None, alias="access_token"),
        refresh_token_from_cookie: str | None = fastapi.Cookie(None, alias="refresh_token"),
        access_token_from_header: str | None = fastapi.Header(None, alias="Authorization"),
) -> uuid.UUID:
    access_token, refresh_token = None, None

    if access_token_from_header is not None and access_token_from_header.startswith("Bearer "):
        access_token = access_token_from_header.lstrip("Bearer").strip()
    if access_token is None:
        access_token = access_token_from_cookie
    if refresh_token is None:
        refresh_token = refresh_token_from_cookie

    jwt_methods: JWTMethods = websocket.app.service.jwt_methods

    user_id = None
    if access_token is not None:
        user_id = jwt_methods.decode_access_token(access_token)
    if user_id is None:
        if refresh_token is None:
            raise HTTPNotAuthenticated()
        user_id = jwt_methods.decode_refresh_token(refresh_token)
        if user_id is None:
            raise HTTPNotAuthenticated()

    return user_id

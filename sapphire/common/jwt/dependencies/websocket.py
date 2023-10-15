import uuid

import fastapi

from sapphire.common.api.exceptions import HTTPNotAuthenticated
from sapphire.common.jwt.methods import JWTMethods


async def get_request_user_id(
        websocket: fastapi.WebSocket,
        access_token_from_cookie: str | None = fastapi.Cookie(None, alias="access_token"),
        refresh_token_from_cookie: str | None = fastapi.Cookie(None, alias="refresh_token"),
        access_token_from_header: str | None = fastapi.Header(None, alias="Authorization"),
) -> uuid.UUID | None:
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
            return None
        user_id = jwt_methods.decode_refresh_token(refresh_token)

    return user_id


async def auth_user_id(user_id: uuid.UUID | None = fastapi.Depends(get_request_user_id)) -> uuid.UUID:
    if user_id is None:
        raise HTTPNotAuthenticated

    return user_id

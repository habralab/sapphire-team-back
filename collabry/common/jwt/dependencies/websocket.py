import fastapi

from collabry.common.api.exceptions import HTTPForbidden, HTTPNotAuthenticated
from collabry.common.jwt.methods import JWTMethods
from collabry.common.jwt.models import JWTData


async def get_jwt_data(
        websocket: fastapi.WebSocket,
        access_token_from_cookie: str | None = fastapi.Cookie(None, alias="access_token"),
        refresh_token_from_cookie: str | None = fastapi.Cookie(None, alias="refresh_token"),
        access_token_from_header: str | None = fastapi.Header(None, alias="Authorization"),
) -> JWTData | None:
    access_token, refresh_token = None, None

    if access_token_from_header is not None and access_token_from_header.startswith("Bearer "):
        access_token = access_token_from_header.lstrip("Bearer").strip()
    if access_token is None:
        access_token = access_token_from_cookie
    if refresh_token is None:
        refresh_token = refresh_token_from_cookie

    jwt_methods: JWTMethods = websocket.app.service.jwt_methods

    jwt_data = None
    if access_token is not None:
        jwt_data = jwt_methods.decode_access_token(access_token)
    if jwt_data is None:
        if refresh_token is None:
            return None
        jwt_data = jwt_methods.decode_refresh_token(refresh_token)

    return jwt_data


async def is_auth(jwt_data: JWTData | None = fastapi.Depends(get_jwt_data)) -> JWTData:
    if jwt_data is None:
        raise HTTPNotAuthenticated()

    return jwt_data


async def is_activated(jwt_data: JWTData = fastapi.Depends(is_auth)) -> JWTData:
    if not jwt_data.is_activated:
        raise HTTPForbidden()

    return jwt_data

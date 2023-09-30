import datetime

import fastapi
import jwt
from pydantic import BaseModel

from sapphire.users.settings import UsersSettings


class JWTDecodePayload(BaseModel):
    success_decode: bool
    error: str | None = None
    user_id: str | None = None


class JWTMethods:
    __access_token_expires: datetime.timedelta = datetime.timedelta(minutes=5)
    __refresh_token_expires: datetime.timedelta = datetime.timedelta(days=30)

    def __init__(
        self,
        access_token_public_key,
        access_token_private_key,
        refresh_token_public_key,
        refresh_token_private_key,
    ):
        self.access_token_public_key = access_token_public_key
        self.access_token_private_key = access_token_private_key
        self.refresh_token_public_key = refresh_token_public_key
        self.refresh_token_private_key = refresh_token_private_key

    def set_expires_for_token(self, access_token_expires, refresh_token_expires):
        self.__access_token_expires = access_token_expires
        self.__refresh_token_expires = refresh_token_expires

    def issue_access_token(self, user_id: str):
        return jwt.encode(
            {"user_id": user_id},
            self.access_token_private_key,
            algorithm="RS256",
        )

    def get_access_token_payload(self, access_token: str):
        try:
            return JWTDecodePayload(
                success_decode=True,
                **jwt.decode(
                    access_token,
                    self.access_token_public_key,
                    algorithms=["RS256"],
                    options={"require": ["user_id"]},
                ),
            )
        except jwt.PyJWTError as jwt_error:
            return JWTDecodePayload(
                success_decode=False, error=jwt_error.__class__.__name__
            )

    def issue_refresh_token(self, user_id: str):
        return jwt.encode(
            {"user_id": user_id},
            self.refresh_token_private_key,
            algorithm="RS256",
        )

    def get_refresh_token_payload(self, refresh_token: str):
        try:
            return JWTDecodePayload(
                success_decode=True,
                **jwt.decode(
                    refresh_token,
                    self.refresh_token_public_key,
                    algorithms=["RS256"],
                    options={"require": ["user_id"]},
                ),
            )
        except jwt.PyJWTError as jwt_error:
            return JWTDecodePayload(
                success_decode=False, error=jwt_error.__class__.__name__
            )

    @property
    def access_token_expires(self):
        return int(self.__access_token_expires.total_seconds())

    @property
    def refresh_token_expires(self):
        return int(self.__refresh_token_expires.total_seconds())


def get_jwt_methods(settings: UsersSettings):
    jwt_methods = JWTMethods(
        access_token_private_key=settings.jwt_access_token_private_key,
        access_token_public_key=settings.jwt_access_token_public_key,
        refresh_token_private_key=settings.jwt_refresh_token_private_key,
        refresh_token_public_key=settings.jwt_refresh_token_public_key,
    )
    jwt_methods.set_expires_for_token(
        access_token_expires=settings.jwt_access_token_expires,
        refresh_token_expires=settings.jwt_access_token_expires,
    )
    return jwt_methods


# For FastApi Depends
def verify_jwt_tokens(response: fastapi.Response, request: fastapi.Request):
    access_token = request.cookies.get("access_token")
    refresh_token = request.cookies.get("refresh_token")
    jwt_methods: JWTMethods = request.app.service.jwt_methods

    if access_token is None:
        if refresh_token is None:
            raise fastapi.HTTPException(status_code=403, detail="Missing tokens")
        refresh_token_payload = jwt_methods.get_refresh_token_payload(refresh_token)
        if not refresh_token_payload.success_decode:
            raise fastapi.HTTPException(
                status_code=403, detail=f"Received error: {refresh_token_payload.error}"
            )
        # Update access token
        new_access_token = jwt_methods.issue_access_token(refresh_token_payload.user_id)
        response.set_cookie(
            key="access_token",
            value=new_access_token,
            expires=jwt_methods.access_token_expires,
            path="/",
            secure=True,
            httponly=True,
            samesite="none",
        )
    else:
        access_token_payload = jwt_methods.get_access_token_payload(access_token)
        if not access_token_payload.success_decode:
            raise fastapi.HTTPException(
                status_code=403, detail=f"Received error: {access_token_payload.error}"
            )
    # verify is ok


# For FastApi Depends
def parse_user_id(request: fastapi.Request):
    jwt_methods: JWTMethods = request.app.service.jwt_methods
    access_token = request.cookies.get("access_token")
    refresh_token = request.cookies.get("refresh_token")
    access_token_payload = jwt_methods.get_access_token_payload(access_token)
    refresh_token_payload = jwt_methods.get_refresh_token_payload(refresh_token)
    return access_token_payload.user_id | refresh_token_payload.user_id

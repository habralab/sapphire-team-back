import datetime
import uuid

import jwt
from pydantic import ValidationError

from .models import JWTData
from .settings import JWTSettings


class JWTMethods:
    def __init__(
        self,
        access_token_public_key: str,
        access_token_private_key: str,
        refresh_token_public_key: str,
        refresh_token_private_key: str,
        access_token_expires: datetime.timedelta,
        refresh_token_expires: datetime.timedelta,
    ) -> None:
        self.access_token_public_key: str = access_token_public_key
        self.access_token_private_key: str = access_token_private_key
        self.refresh_token_public_key: str = refresh_token_public_key
        self.refresh_token_private_key: str = refresh_token_private_key
        self.access_token_expires: datetime.timedelta = access_token_expires
        self.refresh_token_expires: datetime.timedelta = refresh_token_expires

    @property
    def access_token_expires_utc(self) -> datetime.datetime:
        return datetime.datetime.utcnow() + self.access_token_expires

    @property
    def refresh_token_expires_utc(self) -> datetime.datetime:
        return datetime.datetime.utcnow() + self.refresh_token_expires

    def issue_access_token(self, user_id: uuid.UUID, is_activated: bool) -> str:
        return jwt.encode(
            {
                "user_id": str(user_id),
                "is_activated": is_activated,
                "exp": datetime.datetime.now() + self.access_token_expires,
            },
            self.access_token_private_key,
            algorithm="RS256",
        )

    def decode_access_token(self, access_token: str) -> JWTData | None:
        try:
            data = jwt.decode(
                access_token,
                self.access_token_public_key,
                algorithms=["RS256"],
                options={"require": ["user_id", "is_activated"]},
            )
            return JWTData.model_validate(data)
        except (jwt.PyJWTError, ValidationError):
            return None

    def issue_refresh_token(self, user_id: uuid.UUID, is_activated: bool) -> str:
        return jwt.encode(
            {
                "user_id": str(user_id),
                "is_activated": is_activated,
                "exp": datetime.datetime.now() + self.refresh_token_expires,
            },
            self.refresh_token_private_key,
            algorithm="RS256",
        )

    def decode_refresh_token(self, refresh_token: str) -> JWTData | None:
        try:
            data = jwt.decode(
                refresh_token,
                self.refresh_token_public_key,
                algorithms=["RS256"],
                options={"require": ["user_id", "is_activated"]},
            )
            return JWTData.model_validate(data)
        except (jwt.PyJWTError, ValidationError):
            return None


def get_jwt_methods(settings: JWTSettings) -> JWTMethods:
    return JWTMethods(
        access_token_private_key=settings.jwt_access_token_private_key,
        access_token_public_key=settings.jwt_access_token_public_key,
        refresh_token_private_key=settings.jwt_refresh_token_private_key,
        refresh_token_public_key=settings.jwt_refresh_token_public_key,
        access_token_expires=settings.jwt_access_token_expires,
        refresh_token_expires=settings.jwt_refresh_token_expires,
    )

import secrets
import uuid

from pydantic import EmailStr

from collabry.common.cache.service import BaseCacheService

from .settings import Settings


class Service(BaseCacheService):
    def __init__(self, url: str, oauth2_state_ttl: int = 120, reset_password_code_ttl: int = 86400):
        super().__init__(url=url)

        self._oauth2_state_ttl = oauth2_state_ttl
        self._reset_password_code_ttl = reset_password_code_ttl

    async def oauth_set_state(self) -> str:
        state = str(uuid.uuid4())
        key = f"users:auth:oauth2:habr:state:{state}"
        await self.redis.set(key, state, ex=self._reset_password_code_ttl)
        return state

    async def oauth_validate_state(self, state: str) -> bool:
        key = f"users:auth:oauth2:habr:state:{state}"
        value = await self.redis.get(key)
        if value is not None:
            await self.redis.delete(key)
            return True
        return False

    async def reset_password_set_code(self, email: EmailStr) -> str:
        code = str(secrets.token_urlsafe(12))  # generate sixteen-digit secret code
        key = f"users:auth:change_password:secret_code:{email}"
        await self.redis.set(key, code, ex=self._reset_password_code_ttl)
        return code

    async def reset_password_validate_code(self, email: EmailStr, code: str) -> bool:
        key = f"users:auth:change_password:secret_code:{email}"
        value = await self.redis.get(key)
        if value == code:
            await self.redis.delete(key)
            return True
        return False


def get_service(settings: Settings) -> Service:
    return Service(
        url=str(settings.url),
        oauth2_state_ttl=settings.oauth2_state_ttl,
        reset_password_code_ttl=settings.reset_password_code_ttl,
    )

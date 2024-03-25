import secrets
import uuid

from sapphire.common.cache.service import BaseCacheService

from .settings import Settings


class Service(BaseCacheService):
    async def oauth_set_state(self) -> str:
        state = str(uuid.uuid4())
        key = f"users:auth:oauth2:habr:state:{state}"
        await self.redis.set(key, state, ex=120)
        return state

    async def oauth_validate_state(self, state: str) -> bool:
        key = f"users:auth:oauth2:habr:state:{state}"
        value = await self.redis.get(key)
        if value is not None:
            await self.redis.delete(key)
            return True
        return False

    async def change_password_set_secret_code(self) -> str:
        secret_code = str(secrets.token_urlsafe(12))
        key = f"users:auth:change_password:secret_code:{secret_code}"
        await self.redis.set(key, secret_code, ex=43200)
        return secret_code

    async def change_password_validate_code(self, secret_code: str) -> None:
        key = f"users:auth:change_password:secret_code:{secret_code}"
        sent_code = await self.redis.get(key)
        return sent_code




def get_service(settings: Settings) -> Service:
    return Service(url=str(settings.url))

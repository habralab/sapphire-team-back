import uuid

from sapphire.common.cache.service import BaseCacheService

from .settings import Settings


class Service(BaseCacheService):
    async def set_state(self) -> str:
        state = str(uuid.uuid4())
        key = f"users:auth:oauth2:habr:state:{state}"
        await self.redis.set(key, state, ex=120)
        return state

    async def validate_state(self, state: str) -> bool:
        key = f"users:auth:oauth2:habr:state:{state}"
        value = await self.redis.get(key)
        if value is not None:
            await self.redis.delete(key)
            return True
        return False


def get_service(settings: Settings) -> Service:
    return Service(url=str(settings.url))

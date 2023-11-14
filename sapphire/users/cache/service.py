import uuid

from sapphire.common.cache.service import BaseCacheService
from sapphire.users.settings import UsersSettings


class UsersCacheService(BaseCacheService):
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


def get_service(settings: UsersSettings) -> UsersCacheService:
    return UsersCacheService(cache_url=settings.cache_url)

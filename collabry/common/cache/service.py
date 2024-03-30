from typing import Any

from facet import ServiceMixin
from redis import asyncio as aioredis


class BaseCacheService(ServiceMixin):
    def __init__(self, url: str):
        self.url = url
        self.redis = None

    async def start(self):
        self.redis = aioredis.from_url(self.url)

    async def stop(self):
        if self.redis:
            await self.redis.close()
            self.redis = None

    async def set(self, key: str, value: Any):
        await self.redis.set(key, value)

    async def get(self, key: str):
        await self.redis.get(key)

    async def delete(self, key: str):
        await self.redis.delete(key)

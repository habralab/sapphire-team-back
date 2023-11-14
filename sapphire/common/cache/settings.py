from pydantic import AnyUrl
from pydantic_settings import BaseSettings


class BaseCacheSettings(BaseSettings):
    cache_url: AnyUrl = AnyUrl("redis://localhost:6379/0")

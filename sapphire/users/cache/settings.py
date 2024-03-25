from sapphire.common.cache.settings import BaseCacheSettings


class Settings(BaseCacheSettings):
    oauth_storage_time: int = 120
    code_storage_time: int = 43200

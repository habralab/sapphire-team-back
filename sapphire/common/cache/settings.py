from pydantic import AnyUrl, BaseModel


class BaseCacheSettings(BaseModel):
    url: AnyUrl = AnyUrl("redis://localhost:6379/0")

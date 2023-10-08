from pydantic import AnyHttpUrl, conint
from pydantic_settings import BaseSettings


class BaseAPISettings(BaseSettings):
    port: conint(ge=1, le=65535) = 8000
    root_url: AnyHttpUrl = AnyHttpUrl("http://localhost:8000")
    root_path: str = ""
    allowed_origins: list[str] = []

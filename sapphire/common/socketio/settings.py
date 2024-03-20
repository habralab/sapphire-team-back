from pydantic import conint
from pydantic_settings import BaseSettings


class BaseSocketIOSettings(BaseSettings):
    port: conint(ge=1, le=65535) = 8080
    root_path: str = ""
    allowed_origins: list[str] = []

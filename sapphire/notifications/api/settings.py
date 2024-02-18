from pydantic import conint

from sapphire.common.api.settings import BaseAPISettings


class Settings(BaseAPISettings):
    port: conint(ge=1, le=65535) = 8010

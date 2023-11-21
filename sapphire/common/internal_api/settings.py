from pydantic import conint
from pydantic_settings import BaseSettings


class BaseInternalAPISettings(BaseSettings):
    grpc_port: conint(ge=1, le=65535) = 50051
    grpc_reflection: bool = False

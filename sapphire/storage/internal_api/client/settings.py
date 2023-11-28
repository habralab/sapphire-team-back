from pydantic import conint
from pydantic_settings import BaseSettings


class StorageInternalAPIClientSettings(BaseSettings):
    storage_grpc_host: str = "localhost"
    storage_grpc_port: conint(ge=1, le=65535) = 50051

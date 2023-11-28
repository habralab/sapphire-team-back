from pydantic import conint
from pydantic_settings import BaseSettings


class UsersInternalAPIClientSettings(BaseSettings):
    users_grpc_host: str = "localhost"
    users_grpc_port: conint(ge=1, le=65535) = 50051

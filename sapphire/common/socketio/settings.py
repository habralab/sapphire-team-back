from pydantic import conint
from pydantic_settings import BaseSettings


class BaseSocketIOSettings(BaseSettings):
    socketio_port: conint(ge=1, le=65535) = 8080
    socketio_root_path: str = "socketio"
    socketio_allowed_origins: list[str] = []

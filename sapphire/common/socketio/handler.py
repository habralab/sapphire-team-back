from typing import Any

from pydantic import BaseModel


class BaseSocketIOHandler(BaseModel):
    name: str
    handler: Any

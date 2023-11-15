import uuid

from pydantic import BaseModel


class Email(BaseModel):
    type: str
    to: list[uuid.UUID]

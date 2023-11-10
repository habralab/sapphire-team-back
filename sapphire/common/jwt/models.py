import uuid

from pydantic import BaseModel


class JWTData(BaseModel):
    user_id: uuid.UUID
    is_activated: bool

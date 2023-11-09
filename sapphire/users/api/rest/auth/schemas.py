import uuid

from pydantic import BaseModel


class AuthorizeResponse(BaseModel):
    user_id: uuid.UUID
    access_token: str
    refresh_token: str

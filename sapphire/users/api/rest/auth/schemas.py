from pydantic import BaseModel

from sapphire.users.api.rest.schemas import UserResponse


class AuthorizeResponse(BaseModel):
    user: UserResponse
    access_token: str
    refresh_token: str

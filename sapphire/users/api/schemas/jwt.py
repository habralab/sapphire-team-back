from pydantic import BaseModel


class JWTTokensResponse(BaseModel):
    access_token: str
    refresh_token: str

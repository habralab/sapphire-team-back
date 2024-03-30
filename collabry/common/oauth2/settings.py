from pydantic import BaseModel


class BaseOAuth2Settings(BaseModel):
    client_id: str = ""
    client_secret: str = ""

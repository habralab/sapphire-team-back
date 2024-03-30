
from pydantic import BaseModel


class HabrSettings(BaseModel):
    api_key: str = ""

from pydantic import BaseModel


class HabrCareerSettings(BaseModel):
    api_key: str = ""

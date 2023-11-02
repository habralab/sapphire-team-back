from pydantic_settings import BaseSettings


class HabrCareerSettings(BaseSettings):
    habr_career_api_key: str = ""

from pydantic_settings import BaseSettings


class HabrSettings(BaseSettings):
    habr_api_key: str = ""

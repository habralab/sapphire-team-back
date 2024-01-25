from pydantic import EmailStr, conint
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    email_sender: EmailStr = "user@example.com"
    email_hostname: str = "smtp.gmail.com"
    email_port: conint(ge=1, le=65535) = 587
    email_start_tls: bool = False
    email_tls: bool = False


def get_settings() -> Settings:
    return Settings()

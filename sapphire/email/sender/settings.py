from pydantic import EmailStr, conint
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", secrets_dir="/run/secrets", extra="ignore")

    email_sender: EmailStr = "user@example.com"
    email_hostname: str = "smtp.gmail.com"
    email_port: conint(ge=1, le=65535) = 587
    email_start_tls: bool = False
    email_tls: bool = False


def get_settings() -> Settings:
    return Settings()

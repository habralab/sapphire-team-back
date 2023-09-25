from pydantic import AnyUrl, conint
from pydantic_settings import BaseSettings
from fastapi import FastAPI


class UsersSettings(BaseSettings):
    port: conint(ge=1, le=65535) = 8000

    db_dsn: AnyUrl = AnyUrl("sqlite+aiosqlite:///users.sqlite3")


def get_settings() -> UsersSettings:
    return UsersSettings()


app = FastAPI()


class BaseConfig(BaseSettings):
    my_id: str
    my_secret: str


class Config:
    case_sensitive = False
    secrets_dir = "/run/secrets"
    # id_dir =


APP_SETTING = BaseConfig()


@app.get("/")
async def root():
    return {"data": APP_SETTING}
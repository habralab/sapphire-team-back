from pydantic import AnyUrl
from pydantic_settings import BaseSettings


class BaseDatabaseSettings(BaseSettings):
    db_dsn: AnyUrl

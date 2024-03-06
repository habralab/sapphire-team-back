from pydantic import AnyUrl, BaseModel


class BaseDatabaseSettings(BaseModel):
    dsn: AnyUrl

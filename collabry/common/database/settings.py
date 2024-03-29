from pydantic import AnyUrl, BaseModel, PositiveInt


class BaseDatabaseSettings(BaseModel):
    dsn: AnyUrl
    pool_size: PositiveInt = 5
    pool_recycle: PositiveInt = 60  # in seconds: 1 minute

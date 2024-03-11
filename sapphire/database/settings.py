from pydantic import AnyUrl, BaseModel


class Settings(BaseModel):
    dsn: AnyUrl = AnyUrl("sqlite+aiosqlite:///db.sqlite3")

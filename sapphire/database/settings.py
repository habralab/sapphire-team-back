from pydantic import AnyUrl

from sapphire.common.database.settings import BaseDatabaseSettings


class Settings(BaseDatabaseSettings):
    dsn: AnyUrl = AnyUrl("sqlite+aiosqlite:///db.sqlite3")

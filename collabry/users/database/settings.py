from pydantic import AnyUrl

from collabry.common.database.settings import BaseDatabaseSettings


class Settings(BaseDatabaseSettings):
    dsn: AnyUrl = AnyUrl("sqlite+aiosqlite:///users.sqlite3")

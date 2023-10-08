import pathlib
import uuid
from typing import Optional

from sapphire.common.database.service import BaseDatabaseService
from sapphire.users.database.models import User
from sapphire.users.settings import UsersSettings


class UsersDatabaseService(BaseDatabaseService):
    def get_alembic_config_path(self) -> pathlib.Path:
        return pathlib.Path(__file__).parent / "migrations"

    async def get_or_create_user(
        user_id: uuid.UUID,
        user_email: str,
        user_first_name: Optional[str] = None,
        user_last_name: Optional[str] = None,
        user_avatar: Optional[str] = None,
    ) -> User:
        async with self._sessionmaker() as session:
            user_in_db = await session.query(User).filter(
                User.email == user_email
            ).first()
            if not user_in_db:
                user = User(
                    id=user_id,
                    email=user_email,
                    first_name=user_first_name,
                    last_name=user_last_name
                )
                await session.add(user)
                await session.commit()
            return user_in_db
 

def get_service(settings: UsersSettings) -> UsersDatabaseService:
    return UsersDatabaseService(dsn=str(settings.db_dsn))

import pathlib

from sapphire.common.database.service import BaseDatabaseService
from sapphire.users.database.models import User
from sapphire.users.oauth2.habr import HabrUser
from sapphire.users.settings import UsersSettings


class UsersDatabaseService(BaseDatabaseService):
    def get_alembic_config_path(self) -> pathlib.Path:
        return pathlib.Path(__file__).parent / "migrations"

    async def create_user(self, user_info: HabrUser):
        async with self.database_service._sessionmaker() as session:
            user_in_db = await session.query(User).filter(
                User.email == user_info.email
            ).first()
            if not user_in_db:
                user = User(
                    id=user_info.id,
                    email=user_info.email,
                    first_name=user_info.login,
                )
                session.add(user)
            await session.commit()


def get_service(settings: UsersSettings) -> UsersDatabaseService:
    return UsersDatabaseService(dsn=str(settings.db_dsn))

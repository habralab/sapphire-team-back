import pathlib
import uuid
from typing import Type

from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from sapphire.common.database.service import BaseDatabaseService
from sapphire.common.utils.empty import Empty
from sapphire.messenger.settings import MessengerSettings

from .models import Base, Chat, Member, Message


class MessengerDatabaseService(BaseDatabaseService):
    def get_alembic_config_path(self) -> pathlib.Path:
        return pathlib.Path(__file__).parent / "migrations"

    def get_fixtures_directory_path(self) -> pathlib.Path:
        return pathlib.Path(__file__).parent / "fixtures"

    def get_models(self) -> list[Type[Base]]:
        return [Chat, Member, Message]

    async def get_chats(
            self,
            session: AsyncSession,
            user_id: uuid.UUID,
            members: set[uuid.UUID] | Type[Empty] = Empty,
    ) -> list[Chat]:
        query = select(Chat).where(Member.user_id == user_id, Member.chat_id == Chat.id)

        filters = []
        if members is not Empty and len(members) > 0:
            filters.append(or_(*(Member.user_id == member for member in members)))
        query = query.where(*filters)

        result = await session.execute(query)

        return list(result.unique().scalars().all())

    async def create_chat(
            self,
            session: AsyncSession,
            is_personal: bool,
            members_ids: list[uuid.UUID]
    ) -> Chat:
        chat = Chat(is_personal=is_personal)

        for member_id in members_ids:
            member = Member(user_id=member_id)
            chat.members.append(member)

        session.add(chat)

        return chat


def get_service(settings: MessengerSettings) -> MessengerDatabaseService:
    return MessengerDatabaseService(dsn=str(settings.db_dsn))

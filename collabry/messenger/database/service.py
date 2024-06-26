import uuid
from typing import Type

from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from collabry.common.database.service import BaseDatabaseService
from collabry.common.utils.empty import Empty
from collabry.database.models import Chat, ChatMember, Message

from .settings import Settings


class Service(BaseDatabaseService):  # pylint: disable=abstract-method
    async def _get_chats_filters(
        self,
        user_id: uuid.UUID,
        members: set[uuid.UUID] | Type[Empty] = Empty,
    ) -> list:
        filters = [ChatMember.user_id == user_id, ChatMember.chat_id == Chat.id]
        if members is not Empty and len(members) > 0:
            filters.append(or_(*(ChatMember.user_id == member for member in members)))

        return filters

    async def get_chats_count(
            self,
            session: AsyncSession,
            user_id: uuid.UUID,
            members: set[uuid.UUID] | Type[Empty] = Empty,
    ) -> int:
        query = select(func.count(Chat.id)) # pylint: disable=not-callable

        filters = await self._get_chats_filters(user_id=user_id, members=members)
        query = query.where(*filters)

        result = await session.scalar(query)

        return result

    async def get_chats(
            self,
            session: AsyncSession,
            user_id: uuid.UUID,
            members: set[uuid.UUID] | Type[Empty] = Empty,
            page: int = 1,
            per_page: int = 10,
    ) -> list[Chat]:
        query = select(Chat).order_by(Chat.created_at.desc())

        filters = await self._get_chats_filters(user_id=user_id, members=members)
        query = query.where(*filters)

        offset = (page - 1) * per_page
        query = query.limit(per_page).offset(offset)

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
            member = ChatMember(user_id=member_id)
            chat.members.append(member)

        session.add(chat)

        return chat

    async def get_chat(self, session: AsyncSession, chat_id: uuid.UUID) -> Chat | None:
        query = select(Chat).where(Chat.id == chat_id)
        result = await session.execute(query)

        return result.unique().scalar_one_or_none()

    async def get_chat_messages_count(self, session: AsyncSession, chat_id: uuid.UUID) -> int:
        query = (
            select(func.count(Message.id)).where(Message.chat_id == chat_id) # pylint: disable=not-callable
        )
        result = await session.scalar(query)

        return result

    async def get_chat_messages(
            self,
            session: AsyncSession,
            chat_id: uuid.UUID,
            page: int = 1,
            per_page: int = 10,
    ) -> list[Message]:
        query = (
            select(Message).where(Message.chat_id == chat_id).order_by(Message.created_at.desc())
        )

        offset = (page - 1) * per_page
        query = query.limit(per_page).offset(offset)

        result = await session.execute(query)

        return list(result.unique().scalars().all())

    async def create_chat_message(
            self,
            session: AsyncSession,
            chat: Chat,
            member_id: uuid.UUID,
            text: str,
    ) -> Message:
        message = Message(chat=chat, member_id=member_id, text=text)

        session.add(message)

        return message

    async def get_chat_message(
            self,
            session: AsyncSession,
            message_id: uuid.UUID,
    ) -> Message | None:
        query = select(Message).where(Message.id == message_id)

        result = await session.execute(query)

        return result.unique().scalar_one_or_none()


def get_service(settings: Settings) -> Service:
    return Service(
        dsn=str(settings.dsn),
        pool_size=settings.pool_size,
        pool_recycle=settings.pool_recycle,
    )

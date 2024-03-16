import fastapi
from loguru import logger

from sapphire.common.api.dependencies.pagination import Pagination, pagination
from sapphire.common.api.exceptions import HTTPInternalServerError
from sapphire.database.models import Chat, ChatMember
from sapphire.messenger import database
from sapphire.messenger.api.rest.chats.dependencies import get_path_chat, path_chat_is_member
from sapphire.messenger.api.rest.chats.messages.schemas import MessageListResponse
from sapphire.messenger.api.rest.chats.schemas import MessageResponse

from .schemas import CreateMessageRequest


async def get_messages(
        request: fastapi.Request,
        chat: Chat = fastapi.Depends(path_chat_is_member),
        pagination: Pagination = fastapi.Depends(pagination),
) -> MessageListResponse:
    database_service: database.Service = request.app.service.database

    async with database_service.transaction() as session:
        db_messages = await database_service.get_chat_messages(
            session=session,
            chat_id=chat.id,
            page=pagination.page,
            per_page=pagination.per_page,
        )
        total_messages = await database_service.get_chat_messages_count(
            session=session, chat_id=chat.id
        )

    total_pages = -(total_messages // -pagination.per_page)
    messages = [MessageResponse.model_validate(db_message) for db_message in db_messages]
    return MessageListResponse(
        data=messages,
        page=pagination.page,
        per_page=pagination.per_page,
        total_items=total_messages,
        total_pages=total_pages,
    )


async def create_message(
        request: fastapi.Request,
        chat: Chat = fastapi.Depends(get_path_chat),
        member: ChatMember = fastapi.Depends(path_chat_is_member),
        data: CreateMessageRequest = fastapi.Body(embed=False),
) -> MessageResponse:
    database_service: database.Service = request.app.service.database

    async with database_service.transaction() as session:
        db_message = await database_service.create_chat_message(
            session=session,
            chat=chat,
            member_id=member.id,
            text=data.text,
        )
    async with database_service.transaction() as session:
        db_message = await database_service.get_chat_message(
            session=session,
            message_id=db_message.id,
        )
    if db_message is None:
        logger.error("Chat message not exist")
        raise HTTPInternalServerError()

    return MessageResponse.from_db_model(db_message)

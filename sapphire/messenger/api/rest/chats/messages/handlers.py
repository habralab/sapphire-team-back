import fastapi

from sapphire.common.api.dependencies.pagination import Pagination, pagination
from sapphire.common.jwt.dependencies.rest import is_auth
from sapphire.common.jwt.models import JWTData
from sapphire.messenger.api.rest.chats.dependencies import path_chat_is_member
from sapphire.messenger.api.rest.chats.messages.schemas import MessageListResponse
from sapphire.messenger.api.rest.chats.schemas import MessageResponse
from sapphire.messenger.database.models import Chat
from sapphire.messenger.database.service import MessengerDatabaseService

from .schemas import CreateMessageRequest


async def get_messages(
        request: fastapi.Request,
        chat: Chat = fastapi.Depends(path_chat_is_member),
        pagination: Pagination = fastapi.Depends(pagination),
) -> MessageListResponse:
    database_service: MessengerDatabaseService = request.app.service.database

    async with database_service.transaction() as session:
        db_messages = await database_service.get_chat_messages(
            session=session,
            chat_id=chat.id,
            cursor=pagination.cursor,
            per_page=pagination.per_page,
        )

    next_cursor = None
    if db_messages:
        next_cursor = db_messages[-1].created_at

    messages = [MessageResponse.model_validate(db_message) for db_message in db_messages]

    return MessageListResponse(
        data=messages, next_cursor=next_cursor, per_page=pagination.per_page
    )


async def create_message(
        request: fastapi.Request,
        jwt_data: JWTData = fastapi.Depends(is_auth),
        chat: Chat = fastapi.Depends(path_chat_is_member),
        data: CreateMessageRequest = fastapi.Body(embed=False),
) -> MessageResponse:
    database_service: MessengerDatabaseService = request.app.service.database

    async with database_service.transaction() as session:
        db_message = await database_service.create_chat_message(
            session=session,
            chat=chat,
            user_id=jwt_data.user_id,
            text=data.text,
        )

    return MessageResponse.model_validate(db_message)

import fastapi

from sapphire.common.api.dependencies.pagination import Pagination, pagination
from sapphire.messenger.api.rest.chats.dependencies import path_chat_is_member
from sapphire.messenger.api.rest.chats.messages.schemas import MessageListResponse
from sapphire.messenger.api.rest.chats.schemas import MessageResponse
from sapphire.messenger.database.models import Chat
from sapphire.messenger.database.service import MessengerDatabaseService


async def get_messages(
        request: fastapi.Request,
        chat: Chat = fastapi.Depends(path_chat_is_member),
        pagination: Pagination = fastapi.Depends(pagination),
) -> MessageListResponse:
    database_service: MessengerDatabaseService = request.app.service.database

    async with database_service.transaction() as session:
        db_messages = await database_service.get_chat_messages(session=session, chat_id=chat.id)

    messages = [MessageResponse.model_validate(db_message) for db_message in db_messages]
    return MessageListResponse(data=messages, page=pagination.page, per_page=pagination.per_page)

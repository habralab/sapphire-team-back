import fastapi

from sapphire.common.api.dependencies.pagination import CursorPagination, cursor_pagination
from sapphire.common.jwt.dependencies.rest import is_auth
from sapphire.common.jwt.models import JWTData
from sapphire.messenger.database.models import Chat
from sapphire.messenger.database.service import MessengerDatabaseService

from .dependencies import path_chat_is_member
from .schemas import ChatListFiltersRequest, ChatListResponse, ChatResponse


async def get_chats(
        request: fastapi.Request,
        jwt_data: JWTData = fastapi.Depends(is_auth),
        filters: ChatListFiltersRequest = fastapi.Depends(ChatListFiltersRequest),
        cursor_pagination: CursorPagination = fastapi.Depends(cursor_pagination),
) -> ChatListResponse:
    database_service: MessengerDatabaseService = request.app.service.database

    async with database_service.transaction() as session:
        db_chats = await database_service.get_chats(
            session=session,
            user_id=jwt_data.user_id,
            members=filters.member,
            cursor=cursor_pagination.cursor,
            per_page=cursor_pagination.per_page,
        )

    chats = [ChatResponse.from_db_model(chat) for chat in db_chats]
    next_cursor = None
    if len(chats):
        next_cursor = chats[-1]

    return ChatListResponse(
        data=chats,
        next_cursor=next_cursor.created_at if next_cursor else None,
        per_page=cursor_pagination.per_page,
    )


async def get_chat(chat: Chat = fastapi.Depends(path_chat_is_member)):
    return ChatResponse.from_db_model(chat)

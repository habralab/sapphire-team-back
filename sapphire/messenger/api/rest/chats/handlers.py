import fastapi

from sapphire.common.api.dependencies.pagination import Pagination, pagination
from sapphire.common.jwt.dependencies.rest import is_auth
from sapphire.common.jwt.models import JWTData
from sapphire.messenger import database
from sapphire.messenger.database.models import Chat

from .dependencies import path_chat_is_member
from .schemas import ChatListFiltersRequest, ChatListResponse, ChatResponse


async def get_chats(
        request: fastapi.Request,
        jwt_data: JWTData = fastapi.Depends(is_auth),
        filters: ChatListFiltersRequest = fastapi.Depends(ChatListFiltersRequest),
        pagination: Pagination = fastapi.Depends(pagination),
) -> ChatListResponse:
    database_service: database.Service = request.app.service.database

    async with database_service.transaction() as session:
        db_chats = await database_service.get_chats(
            session=session,
            user_id=jwt_data.user_id,
            members=filters.member,
            page=pagination.page,
            per_page=pagination.per_page,
        )
        total_chats = await database_service.get_chats_count(
            session=session,
            user_id=jwt_data.user_id,
            members=filters.member,
        )

    total_pages = -(total_chats // -pagination.per_page)

    chats = [ChatResponse.from_db_model(chat) for chat in db_chats]
    return ChatListResponse(
        data=chats,
        page=pagination.page,
        per_page=pagination.per_page,
        total_items=total_chats,
        total_pages=total_pages,
    )


async def get_chat(chat: Chat = fastapi.Depends(path_chat_is_member)):
    return ChatResponse.from_db_model(chat)

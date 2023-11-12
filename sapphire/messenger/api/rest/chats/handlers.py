import fastapi

from sapphire.common.api.dependencies.pagination import Pagination, pagination
from sapphire.common.jwt.dependencies.rest import is_auth
from sapphire.common.jwt.models import JWTData
from sapphire.messenger.database.service import MessengerDatabaseService

from .schemas import ChatListFiltersRequest, ChatListResponse, ChatResponse


async def get_chats(
        request: fastapi.Request,
        jwt_data: JWTData = fastapi.Depends(is_auth),
        filters: ChatListFiltersRequest = fastapi.Depends(ChatListFiltersRequest),
        pagination: Pagination = fastapi.Depends(pagination),
) -> ChatListResponse:
    database_service: MessengerDatabaseService = request.app.service.database

    async with database_service.transaction() as session:
        db_chats = await database_service.get_chats(
            session=session,
            user_id=jwt_data.user_id,
            members=filters.member,
        )

    chats = [ChatResponse.from_db_model(chat) for chat in db_chats]
    return ChatListResponse(data=chats, page=pagination.page, per_page=pagination.per_page)

from sapphire.common.api.schemas.paginated import PaginatedResponse
from sapphire.messenger.api.rest.chats.schemas import MessageResponse


class MessageListResponse(PaginatedResponse):
    data: list[MessageResponse]

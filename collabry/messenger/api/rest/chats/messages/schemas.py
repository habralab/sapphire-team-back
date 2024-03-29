from pydantic import BaseModel, constr

from collabry.common.api.schemas.paginated import PaginatedResponse
from collabry.messenger.api.rest.chats.schemas import MessageResponse


class CreateMessageRequest(BaseModel):
    text: constr(min_length=1, strip_whitespace=True)


class MessageListResponse(PaginatedResponse):
    data: list[MessageResponse]

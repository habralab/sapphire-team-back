import uuid
from typing import Type

from pydantic import BaseModel

from sapphire.common.api.schemas.paginated import PaginatedResponse
from sapphire.common.utils.empty import Empty
from sapphire.storage.api.schemas.specializations import SpecializationGroupResponse


class SpecializationGroupsFilterRequest(BaseModel):
    query_text: str | Type[Empty] = Empty
    id: list[uuid.UUID] | Type[Empty] = Empty
    exclude_id: list[uuid.UUID] | Type[Empty] = Empty


class SpecializationGroupListResponse(PaginatedResponse):
    data: list[SpecializationGroupResponse]

from typing import Type

from pydantic import BaseModel

from sapphire.common.api.schemas.paginated import OffsetPaginatedResponse
from sapphire.common.utils.empty import Empty
from sapphire.storage.api.schemas.specializations import SpecializationGroupResponse


class SpecializationGroupsFilterRequest(BaseModel):
    query_text: str | Type[Empty] = Empty


class SpecializationGroupListResponse(OffsetPaginatedResponse):
    data: list[SpecializationGroupResponse]

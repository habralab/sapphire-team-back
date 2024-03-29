import uuid
from typing import Type

from pydantic import BaseModel

from collabry.common.api.schemas.paginated import PaginatedResponse
from collabry.common.utils.empty import Empty
from collabry.storage.api.schemas.specializations import SpecializationGroupResponse


class SpecializationGroupsFilterRequest(BaseModel):
    query: str | Type[Empty] = Empty
    id: list[uuid.UUID] | Type[Empty] = Empty
    exclude_id: list[uuid.UUID] | Type[Empty] = Empty


class SpecializationGroupListResponse(PaginatedResponse):
    data: list[SpecializationGroupResponse]

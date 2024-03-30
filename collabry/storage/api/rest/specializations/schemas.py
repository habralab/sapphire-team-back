import uuid
from typing import Type

import fastapi
from pydantic import BaseModel, Field

from collabry.common.api.schemas.paginated import PaginatedResponse
from collabry.common.utils.empty import Empty
from collabry.storage.api.schemas.specializations import SpecializationResponse


class SpecializationFiltersRequest(BaseModel):
    query: str | Type[Empty] = Empty
    group_id: uuid.UUID | Type[Empty] = Empty
    id: list[uuid.UUID] | Type[Empty] = Field(fastapi.Query(Empty))
    exclude_id: list[uuid.UUID] | Type[Empty] = Field(fastapi.Query(Empty))


class SpecializationListResponse(PaginatedResponse):
    data: list[SpecializationResponse]

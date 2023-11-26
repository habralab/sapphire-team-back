import uuid
from typing import Type

import fastapi
from pydantic import BaseModel, Field

from sapphire.common.api.schemas.paginated import PaginatedResponse
from sapphire.common.utils.empty import Empty
from sapphire.storage.api.schemas.specializations import SpecializationResponse


class SpecializationFiltersRequest(BaseModel):
    query_text: str | Type[Empty] = Empty
    group_id: uuid.UUID | Type[Empty] = Empty
    id: list[uuid.UUID] | Type[Empty] = Field(fastapi.Query(Empty))


class SpecializationListResponse(PaginatedResponse):
    data: list[SpecializationResponse]

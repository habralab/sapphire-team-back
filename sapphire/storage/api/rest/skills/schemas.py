import uuid
from datetime import datetime
from typing import Type

import fastapi
from pydantic import BaseModel, ConfigDict, Field

from sapphire.common.api.schemas.paginated import OffsetPaginatedResponse
from sapphire.common.utils.empty import Empty


class SkillResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    created_at: datetime


class SkillListResponse(OffsetPaginatedResponse):
    data: list[SkillResponse]


class SkillsFiltersRequest(BaseModel):
    query_text: str | Type[Empty] = Empty
    id: list[uuid.UUID] | Type[Empty] = Field(fastapi.Query(Empty))

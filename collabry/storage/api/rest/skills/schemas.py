import uuid
from datetime import datetime
from typing import Type

import fastapi
from pydantic import BaseModel, ConfigDict, Field

from collabry.common.api.schemas.paginated import PaginatedResponse
from collabry.common.utils.empty import Empty


class SkillResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    created_at: datetime


class SkillListResponse(PaginatedResponse):
    data: list[SkillResponse]


class SkillsFiltersRequest(BaseModel):
    query: str | Type[Empty] = Empty
    id: list[uuid.UUID] | Type[Empty] = Field(fastapi.Query(Empty))
    exclude_id: list[uuid.UUID] | Type[Empty] = Field(fastapi.Query(Empty))

import uuid
from datetime import datetime

import fastapi
from pydantic import BaseModel, ConfigDict, Field

from sapphire.common.api.schemas.paginated import PaginatedResponse
from sapphire.projects.database.models import ProjectStatusEnum


class CreateProjectRequest(BaseModel):
    name: str
    description: str | None
    owner_id: uuid.UUID
    deadline: datetime | None


class ProjectResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    description: str | None
    owner_id: uuid.UUID
    deadline: datetime | None
    created_at: datetime
    updated_at: datetime
    status: ProjectStatusEnum


class ProjectHistoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    project_id: uuid.UUID
    status: ProjectStatusEnum
    created_at: datetime


class ProjectHistoryListResponse(PaginatedResponse):
    data: list[ProjectHistoryResponse]


class ProjectListResponse(PaginatedResponse):
    data: list[ProjectResponse]


class ProjectFiltersRequest(BaseModel):
    query_text: str | None = None
    owner_id: uuid.UUID | None = None
    deadline: datetime | None = None
    status: ProjectStatusEnum | None = None
    position_is_deleted: bool | None = None
    position_is_closed: bool | None = None
    position_skill_ids: list[str] | None = Field(fastapi.Query(None))
    position_specialization_ids: uuid.UUID | None = Field(fastapi.Query(None))

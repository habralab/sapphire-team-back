import uuid
from datetime import datetime

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


class ProjectsResponse(PaginatedResponse):
    data: list[ProjectResponse]


class ProjectFiltersRequest(BaseModel):
    name_substring: str | None = Field(None)
    description_substring: str | None = Field(None)
    owner_id: uuid.UUID | None = Field(None)
    deadline: datetime | None = Field(None)
    status: ProjectStatusEnum | None = Field(None)
    position_name_substring: str | None = Field(None)
    position_is_deleted: bool | None = Field(None)
    position_is_closed: bool | None = Field(None)

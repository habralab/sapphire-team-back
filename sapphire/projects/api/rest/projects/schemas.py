import uuid
from typing import Type

import fastapi
from pydantic import BaseModel, ConfigDict, Field, NaiveDatetime

from sapphire.common.api.schemas.paginated import PaginatedResponse
from sapphire.common.utils.empty import Empty
from sapphire.projects.database.models import ProjectStatusEnum


class CreateProjectRequest(BaseModel):
    name: str
    description: str | None
    owner_id: uuid.UUID
    deadline: NaiveDatetime | None


class ProjectResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    description: str | None
    owner_id: uuid.UUID
    deadline: NaiveDatetime | None
    created_at: NaiveDatetime
    updated_at: NaiveDatetime
    status: ProjectStatusEnum


class ProjectHistoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    project_id: uuid.UUID
    status: ProjectStatusEnum
    created_at: NaiveDatetime


class ProjectHistoryListResponse(PaginatedResponse):
    data: list[ProjectHistoryResponse]


class ProjectListResponse(PaginatedResponse):
    data: list[ProjectResponse]


class ProjectFiltersRequest(BaseModel):
    query_text: str | Type[Empty] = Empty
    owner_id: uuid.UUID | Type[Empty] = Empty
    deadline: NaiveDatetime | Type[Empty] = Empty
    status: ProjectStatusEnum | Type[Empty] = Empty
    position_is_closed: bool | Type[Empty] = Empty
    position_skill_ids: list[str] | Type[Empty] = Field(fastapi.Query(Empty))
    position_specialization_ids: list[uuid.UUID] | Type[Empty] = Field(fastapi.Query(Empty))


class ProjectPartialUpdateRequest(BaseModel):
    status: ProjectStatusEnum | Type[Empty] = Empty

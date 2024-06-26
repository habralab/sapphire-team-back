import uuid
from typing import Type

import fastapi
from pydantic import AwareDatetime, BaseModel, ConfigDict, Field

from collabry.common.api.schemas.paginated import PaginatedResponse
from collabry.common.utils.empty import Empty
from collabry.database.models import ParticipantStatusEnum, ProjectStatusEnum
from collabry.projects.api.rest.schemas import ProjectResponse


class ParticipantResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    position_id: uuid.UUID
    user_id: uuid.UUID
    status: ParticipantStatusEnum
    joined_at: AwareDatetime | None
    created_at: AwareDatetime
    updated_at: AwareDatetime


class CreateProjectRequest(BaseModel):
    name: str
    description: str | None = None
    owner_id: uuid.UUID
    startline: AwareDatetime
    deadline: AwareDatetime | None = None


class ProjectHistoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    project_id: uuid.UUID
    status: ProjectStatusEnum
    created_at: AwareDatetime


class ProjectHistoryListResponse(PaginatedResponse):
    data: list[ProjectHistoryResponse]


class ProjectListResponse(PaginatedResponse):
    data: list[ProjectResponse]


class ProjectListFiltersRequest(BaseModel):
    query: str | Type[Empty] = Empty
    owner_id: uuid.UUID | Type[Empty] = Empty
    user_id: uuid.UUID | Type[Empty] = Empty
    startline_ge: AwareDatetime | Type[Empty] = Empty
    startline_le: AwareDatetime | Type[Empty] = Empty
    deadline_ge: AwareDatetime | Type[Empty] = Empty
    deadline_le: AwareDatetime | Type[Empty] = Empty
    status: list[ProjectStatusEnum] | Type[Empty] = Field(fastapi.Query(Empty))
    position_skill_ids: list[uuid.UUID] | Type[Empty] = Field(fastapi.Query(Empty))
    position_specialization_ids: list[uuid.UUID] | Type[Empty] = Field(fastapi.Query(Empty))
    participant_user_ids: list[uuid.UUID] | Type[Empty] = Field(fastapi.Query(Empty))


class ProjectPartialUpdateRequest(BaseModel):
    status: ProjectStatusEnum | Type[Empty] = Empty

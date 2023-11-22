import uuid
from typing import Type

import fastapi
from pydantic import BaseModel, ConfigDict, Field, NaiveDatetime

from sapphire.common.api.schemas.paginated import OffsetPaginatedResponse
from sapphire.common.utils.empty import Empty
from sapphire.projects.database.models import ParticipantStatusEnum, ProjectStatusEnum


class ParticipantResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    position_id: uuid.UUID
    user_id: uuid.UUID
    status: ParticipantStatusEnum
    joined_at: NaiveDatetime | None
    created_at: NaiveDatetime
    updated_at: NaiveDatetime


class CreateProjectRequest(BaseModel):
    name: str
    description: str | None = None
    owner_id: uuid.UUID
    startline: NaiveDatetime
    deadline: NaiveDatetime | None = None


class ProjectResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    description: str | None
    owner_id: uuid.UUID
    startline: NaiveDatetime
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


class ProjectHistoryListResponse(OffsetPaginatedResponse):
    data: list[ProjectHistoryResponse]


class ProjectListResponse(OffsetPaginatedResponse):
    data: list[ProjectResponse]


class ProjectListFiltersRequest(BaseModel):
    query_text: str | Type[Empty] = Empty
    owner_id: uuid.UUID | Type[Empty] = Empty
    user_id: uuid.UUID | Type[Empty] = Empty
    startline_ge: NaiveDatetime | Type[Empty] = Empty
    startline_le: NaiveDatetime | Type[Empty] = Empty
    deadline_ge: NaiveDatetime | Type[Empty] = Empty
    deadline_le: NaiveDatetime | Type[Empty] = Empty
    status: ProjectStatusEnum | Type[Empty] = Empty
    position_skill_ids: list[uuid.UUID] | Type[Empty] = Field(fastapi.Query(Empty))
    position_specialization_ids: list[uuid.UUID] | Type[Empty] = Field(fastapi.Query(Empty))
    participant_user_ids: list[uuid.UUID] | Type[Empty] = Field(fastapi.Query(Empty))


class ProjectPartialUpdateRequest(BaseModel):
    status: ProjectStatusEnum | Type[Empty] = Empty

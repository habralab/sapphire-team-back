import uuid
from datetime import datetime
from typing import Literal, Type

from pydantic import BaseModel, Field, PositiveInt, constr

from autotests.rest.models import PaginatedResponse

from .enums import ParticipantStatusEnum, ProjectStatusEnum


class HealthResponse(BaseModel):
    name: Literal["Projects"]
    version: constr(pattern=r"^\d+\.\d+\.\d+$")


class CreateProjectRequest(BaseModel):
    name: str
    description: str | None
    owner_id: uuid.UUID
    deadline: datetime | None


class ProjectResponse(BaseModel):
    id: uuid.UUID
    name: str
    description: str | None
    owner_id: uuid.UUID
    deadline: datetime | None
    created_at: datetime
    updated_at: datetime
    status: ProjectStatusEnum


class ProjectListResponse(PaginatedResponse):
    data: list[ProjectResponse]


class PositionResponse(BaseModel):
    id: uuid.UUID
    project_id: uuid.UUID
    # TODO: Uncomment after implement specialization_id
    # specialization_id: uuid.UUID
    closed_at: datetime | None
    created_at: datetime
    updated_at: datetime


class CreatePositionRequest(BaseModel):
    specialization_id: uuid.UUID


class UpdateParticipantRequest(BaseModel):
    status: ParticipantStatusEnum


class ParticipantResponse(BaseModel):
    id: uuid.UUID
    position_id: uuid.UUID
    user_id: uuid.UUID
    status: ParticipantStatusEnum
    created_at: datetime
    updated_at: datetime

class ProjectPartialUpdateRequest(BaseModel):
    status: ProjectStatusEnum | None

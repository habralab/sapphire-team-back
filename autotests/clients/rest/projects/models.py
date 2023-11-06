import uuid
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field, NaiveDatetime, NonNegativeInt, confloat, constr

from autotests.rest.models import PaginatedResponse

from .enums import ParticipantStatusEnum, ProjectStatusEnum


class HealthResponse(BaseModel):
    name: Literal["Projects"]
    version: constr(pattern=r"^\d+\.\d+\.\d+$")


class CreateProjectRequest(BaseModel):
    name: str
    description: str | None
    owner_id: uuid.UUID
    deadline: NaiveDatetime | None


class ProjectResponse(BaseModel):
    id: uuid.UUID
    name: str
    description: str | None
    owner_id: uuid.UUID
    deadline: datetime | None
    created_at: NaiveDatetime
    updated_at: NaiveDatetime
    status: ProjectStatusEnum
    joined_participants: list["ProjectParticipantResponse"] | None


class ProjectListResponse(PaginatedResponse):
    data: list[ProjectResponse]


class CreateReviewRequest(BaseModel):
    user_id: uuid.UUID
    rate: int = Field(ge=1, le=5)
    text: str


class ReviewResponse(BaseModel):
    id: uuid.UUID
    project_id: uuid.UUID
    from_user_id: uuid.UUID
    to_user_id: uuid.UUID
    rate: int = Field(ge=1, le=5)
    text: str


class PositionResponse(BaseModel):
    id: uuid.UUID
    project_id: uuid.UUID
    # TODO: Uncomment after implement specialization_id
    # specialization_id: uuid.UUID
    closed_at: datetime | None
    created_at: datetime
    updated_at: datetime


class PositionListResponse(PaginatedResponse):
    data: list[PositionResponse]


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


class UserStatisticResponse(BaseModel):
    ownership_projects_count: NonNegativeInt
    participant_projects_count: NonNegativeInt
    rate: confloat(ge=1, le=5)


class ProjectParticipantResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    position_id: uuid.UUID
    user_id: uuid.UUID
    status: ParticipantStatusEnum
    joined_at: NaiveDatetime | None
    created_at: NaiveDatetime
    updated_at: NaiveDatetime

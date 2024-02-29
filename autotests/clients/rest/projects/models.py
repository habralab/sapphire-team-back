import uuid
from typing import Annotated, Literal

from pydantic import AwareDatetime, BaseModel, Field, NonNegativeInt, constr

from autotests.clients.rest.models import PaginatedResponse

from .enums import ParticipantStatusEnum, ProjectStatusEnum


class HealthResponse(BaseModel):
    name: Literal["Projects"]
    version: constr(pattern=r"^\d+\.\d+\.\d+$")


class CreateProjectRequest(BaseModel):
    name: str
    description: str | None
    owner_id: uuid.UUID | None
    startline: AwareDatetime
    deadline: AwareDatetime | None


class ParticipantResponse(BaseModel):
    id: uuid.UUID
    position_id: uuid.UUID
    user_id: uuid.UUID
    status: ParticipantStatusEnum
    joined_at: AwareDatetime | None
    created_at: AwareDatetime
    updated_at: AwareDatetime


class ProjectResponse(BaseModel):
    id: uuid.UUID
    name: str
    description: str | None
    owner_id: uuid.UUID
    startline: AwareDatetime
    deadline: AwareDatetime | None
    created_at: AwareDatetime
    updated_at: AwareDatetime
    status: ProjectStatusEnum


class ProjectListResponse(PaginatedResponse):
    data: list[ProjectResponse]


class ParticipantListResponse(PaginatedResponse):
    data: list[ParticipantResponse]


class CreateReviewRequest(BaseModel):
    project_id: uuid.UUID
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
    project: ProjectResponse
    specialization_id: uuid.UUID
    skills: list[uuid.UUID]
    closed_at: AwareDatetime | None
    created_at: AwareDatetime
    updated_at: AwareDatetime


class PositionListResponse(PaginatedResponse):
    data: list[PositionResponse]


class CreatePositionRequest(BaseModel):
    project_id: uuid.UUID
    specialization_id: uuid.UUID


class CreateParticipantRequest(BaseModel):
    position_id: uuid.UUID


class UpdateParticipantRequest(BaseModel):
    status: ParticipantStatusEnum


class ProjectPartialUpdateRequest(BaseModel):
    status: ProjectStatusEnum | None


class UserStatisticResponse(BaseModel):
    ownership_projects_count: NonNegativeInt
    participant_projects_count: NonNegativeInt
    rate: Annotated[float, Field(ge=1, le=5)]

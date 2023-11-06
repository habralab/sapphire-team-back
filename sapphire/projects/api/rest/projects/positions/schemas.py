import uuid

from pydantic import BaseModel, ConfigDict, NaiveDatetime

from sapphire.common.api.schemas.paginated import PaginatedResponse


class ProjectPositionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    project_id: uuid.UUID
    closed_at: NaiveDatetime | None
    created_at: NaiveDatetime
    updated_at: NaiveDatetime


class ProjectPositionsResponse(PaginatedResponse):
    data: list[ProjectPositionResponse]


class CreateProjectPositionRequest(BaseModel):
    specialization_id: uuid.UUID

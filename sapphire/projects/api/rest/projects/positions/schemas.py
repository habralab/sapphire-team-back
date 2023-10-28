import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict

from sapphire.common.api.schemas.paginated import PaginatedResponse


class ProjectPositionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    project_id: uuid.UUID
    name: str
    closed_at: datetime | None
    created_at: datetime
    updated_at: datetime


class ProjectPositionsResponse(PaginatedResponse):
    data: list[ProjectPositionResponse]


class CreateProjectPositionRequest(BaseModel):
    specialization_id: uuid.UUID

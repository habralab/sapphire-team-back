import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ProjectPositionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    project_id: uuid.UUID
    name: str
    closed_at: datetime | None
    created_at: datetime
    updated_at: datetime


class CreateProjectPositionRequest(BaseModel):
    name: str

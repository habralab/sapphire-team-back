import uuid
from datetime import datetime

from pydantic import BaseModel


class ProjectPositionResponse(BaseModel):
    id: uuid.UUID
    project_id: uuid.UUID
    name: str
    closed_at: datetime | None
    created_at: datetime
    updated_at: datetime


class CreateProjectPositionRequest(BaseModel):
    name: str

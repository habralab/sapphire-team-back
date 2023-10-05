import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CreateProjectRequest(BaseModel):
    id: uuid.UUID
    name: str
    description: str | None
    owner_id: uuid.UUID
    deadline: datetime | None


class ProjectResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    description: str | None
    owner_id: uuid.UUID
    deadline: datetime | None
    created_at: datetime
    updated_at: datetime

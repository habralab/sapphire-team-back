import uuid

from pydantic import BaseModel, ConfigDict, NaiveDatetime

from sapphire.projects.database.models import ProjectStatusEnum


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

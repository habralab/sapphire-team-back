import uuid

from pydantic import AwareDatetime, BaseModel, ConfigDict

from collabry.database.models import ProjectStatusEnum


class ProjectResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    description: str | None
    owner_id: uuid.UUID
    startline: AwareDatetime
    deadline: AwareDatetime | None
    created_at: AwareDatetime
    updated_at: AwareDatetime
    status: ProjectStatusEnum

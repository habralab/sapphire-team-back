import uuid
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, constr

from autotests.rest.models import PaginatedResponse

from .enums import ProjectStatusEnum


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

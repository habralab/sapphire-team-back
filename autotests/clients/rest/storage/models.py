import uuid
from typing import Literal

from pydantic import AwareDatetime, BaseModel, constr

from autotests.clients.rest.models import PaginatedResponse


class HealthResponse(BaseModel):
    name: Literal["Storage"]
    version: constr(pattern=r"^\d+\.\d+\.\d+$")


class SpecializationGroupResponse(BaseModel):
    id: uuid.UUID
    name: str
    created_at: AwareDatetime


class SpecializationGroupListResponse(PaginatedResponse):
    data: list[SpecializationGroupResponse]


class SpecializationResponse(BaseModel):
    id: uuid.UUID
    name: str
    group_id: uuid.UUID | None
    created_at: AwareDatetime


class SpecializationListResponse(PaginatedResponse):
    data: list[SpecializationResponse]


class SkillResponse(BaseModel):
    id: uuid.UUID
    name: str
    created_at: AwareDatetime


class SkillListResponse(PaginatedResponse):
    data: list[SkillResponse]

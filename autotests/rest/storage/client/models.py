import uuid
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, NonNegativeInt, PositiveInt, constr


class HealthResponse(BaseModel):
    name: Literal["Storage"]
    version: constr(pattern=r"^\d+\.\d+\.\d+$")


class PaginatedResponse(BaseModel):
    data: list
    page: PositiveInt
    per_page: PositiveInt
    total_pages: NonNegativeInt | None
    total_items: NonNegativeInt | None


class SpecializationGroupResponse(BaseModel):
    id: uuid.UUID
    name: str
    created_at: datetime


class SpecializationGroupListResponse(PaginatedResponse):
    data: list[SpecializationGroupResponse]


class SpecializationResponse(BaseModel):
    id: uuid.UUID
    name: str
    is_other: bool
    group_id: uuid.UUID | None
    created_at: datetime


class SpecializationListResponse(PaginatedResponse):
    data: list[SpecializationResponse]


class SkillResponse(BaseModel):
    id: uuid.UUID
    name: str
    created_at: datetime


class SkillListResponse(PaginatedResponse):
    data: list[SkillResponse]

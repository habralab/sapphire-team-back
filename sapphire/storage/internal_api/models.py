import uuid

from pydantic import BaseModel, PositiveInt


class SpecializationGroupRequest(BaseModel):
    habr_id: PositiveInt


class SpecializationGroupResponse(BaseModel):
    id: uuid.UUID
    name: str
    name_en: str
    habr_id: PositiveInt | None


class SpecializationRequest(BaseModel):
    habr_id: PositiveInt


class SpecializationResponse(BaseModel):
    id: uuid.UUID
    name: str
    name_en: str
    habr_id: PositiveInt | None


class SkillRequest(BaseModel):
    habr_id: PositiveInt


class SkillResponse(BaseModel):
    id: uuid.UUID
    name: str
    habr_id: PositiveInt | None

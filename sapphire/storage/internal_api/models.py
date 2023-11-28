import uuid

from pydantic import BaseModel, PositiveInt


class GetSpecializationGroupRequest(BaseModel):
    habr_id: PositiveInt


class SpecializationGroupResponse(BaseModel):
    id: uuid.UUID
    name: str
    name_en: str
    habr_id: PositiveInt | None


class GetSpecializationRequest(BaseModel):
    habr_id: PositiveInt


class SpecializationResponse(BaseModel):
    id: uuid.UUID
    name: str
    name_en: str
    habr_id: PositiveInt | None


class GetSkillRequest(BaseModel):
    habr_id: PositiveInt


class SkillResponse(BaseModel):
    id: uuid.UUID
    name: str
    habr_id: PositiveInt | None

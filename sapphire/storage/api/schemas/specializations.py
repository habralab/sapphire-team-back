import uuid

from pydantic import AwareDatetime, BaseModel, ConfigDict


class SpecializationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str | None
    group_id: uuid.UUID | None
    created_at: AwareDatetime


class SpecializationGroupResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str | None
    created_at: AwareDatetime

import uuid

from pydantic import BaseModel, ConfigDict, NaiveDatetime


class SpecializationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str | None
    is_other: bool
    group_id: uuid.UUID | None
    created_at: NaiveDatetime


class SpecializationGroupResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str | None
    created_at: NaiveDatetime

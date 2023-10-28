import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class SpecializationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str | None
    is_other: bool
    group_id: str | None
    created_at: datetime


class SpecializationGroupResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str | None
    created_at: datetime

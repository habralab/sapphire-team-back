import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class SkillResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str | None
    created_at: datetime

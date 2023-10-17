import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict

from sapphire.storage.database.models import Specialization


class SpecializationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str | None
    is_other: bool
    group_id: str | None
    migrate_to: str | None
    created_at: datetime

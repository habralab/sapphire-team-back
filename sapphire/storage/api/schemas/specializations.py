import uuid
from datetime import datetime

from pydantic import BaseModel

from sapphire.storage.database.models import Specialization


class SpecializationResponse(BaseModel):
    id: uuid.UUID
    name: str | None
    is_other: bool
    group_id: str | None
    migrate_to: str | None
    created_at: datetime

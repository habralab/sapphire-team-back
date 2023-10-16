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

    @classmethod
    def from_db_model(cls, specialization: Specialization) -> "SpecializationResponse":
        return cls(
            id=specialization.id,
            name=specialization.name,
            is_other=specialization.is_other,
            group_id=specialization.group_id,
            migrate_to=specialization.migrate_to,
            created_at=specialization.created_at
        )

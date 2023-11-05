import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict

from sapphire.projects.database.models import ParticipantStatusEnum


class ProjectParticipantResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    position_id: uuid.UUID
    user_id: uuid.UUID
    status: ParticipantStatusEnum
    joined_at: datetime | None
    created_at: datetime
    updated_at: datetime


class UpdateParticipantRequest(BaseModel):
    status: ParticipantStatusEnum

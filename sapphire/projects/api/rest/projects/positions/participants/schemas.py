import uuid

from pydantic import BaseModel, ConfigDict, NaiveDatetime

from sapphire.projects.database.models import ParticipantStatusEnum


class ProjectParticipantResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    position_id: uuid.UUID
    user_id: uuid.UUID
    status: ParticipantStatusEnum
    joined_at: NaiveDatetime | None
    created_at: NaiveDatetime
    updated_at: NaiveDatetime


class UpdateParticipantRequest(BaseModel):
    status: ParticipantStatusEnum

import uuid

from pydantic import BaseModel

from sapphire.projects.database.models import ParticipantStatusEnum


class CreateParticipantRequest(BaseModel):
    position_id: uuid.UUID


class UpdateParticipantRequest(BaseModel):
    status: ParticipantStatusEnum

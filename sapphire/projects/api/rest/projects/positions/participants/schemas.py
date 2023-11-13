from pydantic import BaseModel

from sapphire.projects.database.models import ParticipantStatusEnum


class UpdateParticipantRequest(BaseModel):
    status: ParticipantStatusEnum

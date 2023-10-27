import enum
import uuid

from pydantic import BaseModel, ConfigDict


class ParticipantNotificationData(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: uuid.UUID
    position_id: uuid.UUID
    project_id: uuid.UUID


class ParticipantNotificationType(str, enum.Enum):
    REQUEST = "participant_requested"
    JOINED = "participant_joined"
    OWNER_DECLINED = "owner_declined"
    PARTICIPANT_DECLINED = "participant_declined"
    LEFT = "participant_left"

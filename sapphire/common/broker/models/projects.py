import enum
import uuid

from pydantic import BaseModel, ConfigDict, EmailStr


class ParticipantNotificationData(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    project_id: uuid.UUID
    project_name: str
    position_id: uuid.UUID
    participant_id: uuid.UUID
    participant_email: EmailStr
    owner_id: uuid.UUID
    owner_email: EmailStr


class ParticipantNotificationType(str, enum.Enum):
    REQUESTED = "participant_requested"
    JOINED = "participant_joined"
    OWNER_DECLINED = "owner_declined"
    PARTICIPANT_DECLINED = "participant_declined"
    PARTICIPANT_LEFT = "participant_left"
    OWNER_EXCLUDED = "owner_excluded"

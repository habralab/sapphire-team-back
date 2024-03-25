import enum
import uuid

from pydantic import BaseModel, EmailStr

from sapphire.common.utils import empty


class EmailType(str, enum.Enum):
    PARTICIPANT_REQUESTED = "participant_requested"
    PARTICIPANT_JOINED = "participant_joined"
    OWNER_DECLINED = "owner_declined"
    PARTICIPANT_DECLINED = "participant_declined"
    PARTICIPANT_LEFT = "participant_left"
    OWNER_EXCLUDED = "owner_excluded"
    RESET_PASSWORD = "change_password"


class Email(BaseModel):
    type: EmailType
    to: list[EmailStr]
    sending_data: dict = {}

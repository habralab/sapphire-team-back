import enum
import uuid

from pydantic import BaseModel

from sapphire.common.utils import empty


class EmailType(str, enum.Enum):
    PARTICIPANT_REQUESTED = "participant_requested"
    PARTICIPANT_JOINED = "participant_joined"
    OWNER_DECLINED = "owner_declined"
    PARTICIPANT_DECLINED = "participant_declined"
    PARTICIPANT_LEFT = "participant_left"
    OWNER_EXCLUDED = "owner_excluded"
    CHANGE_PASSWORD = "change_password"


class Email(BaseModel):
    type: EmailType
    to: list[str]
    sending_data: str = empty.Empty

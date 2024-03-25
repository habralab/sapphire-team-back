import enum
from typing import Any

from pydantic import BaseModel, EmailStr


class EmailType(str, enum.Enum):
    PARTICIPANT_REQUESTED = "participant_requested"
    PARTICIPANT_JOINED = "participant_joined"
    OWNER_DECLINED = "owner_declined"
    PARTICIPANT_DECLINED = "participant_declined"
    PARTICIPANT_LEFT = "participant_left"
    OWNER_EXCLUDED = "owner_excluded"
    RESET_PASSWORD = "reset_password"


class Email(BaseModel):
    type: EmailType
    to: list[EmailStr]
    data: dict[str, Any] = {}

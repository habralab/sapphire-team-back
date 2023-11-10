import enum

from pydantic import BaseModel


class GenderEnum(str, enum.Enum):
    MALE = "male"
    FEMALE = "female"


class UserCard(BaseModel):
    username: str
    full_name: str | None
    avatar: str | None
    speciality: str | None
    gender: GenderEnum | None

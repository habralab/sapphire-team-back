import enum

from pydantic import AnyHttpUrl, BaseModel


class GenderEnum(str, enum.Enum):
    MALE = "male"
    FEMALE = "female"


class UserCard(BaseModel):
    username: str
    full_name: str | None
    avatar: AnyHttpUrl | None
    speciality: str | None
    gender: GenderEnum | None

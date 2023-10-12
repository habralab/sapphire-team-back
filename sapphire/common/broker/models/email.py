from typing import Any

from pydantic import BaseModel, EmailStr


class Email(BaseModel):
    type: str
    to: list[EmailStr]
    data: dict[str, Any]

import uuid

from pydantic import BaseModel


class UserUpdateRequest(BaseModel):
    first_name: str | None
    last_name: str | None
    about: str | None
    main_specialization_id: uuid.UUID | None
    secondary_specialization_id: uuid.UUID | None

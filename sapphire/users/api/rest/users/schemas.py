import uuid

from pydantic import BaseModel, constr


class UserUpdateRequest(BaseModel):
    first_name: constr(strip_whitespace=True, min_length=1)
    last_name: constr(strip_whitespace=True, min_length=1)
    about: str | None
    main_specialization_id: uuid.UUID | None
    secondary_specialization_id: uuid.UUID | None

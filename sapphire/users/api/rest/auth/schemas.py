from pydantic import BaseModel, EmailStr, constr

from sapphire.users.api.rest.schemas import UserResponse


class AuthorizeRequest(BaseModel):
    email: EmailStr
    password: constr(pattern=r"^[\w\(\)\[\]\{\}\^\$\+\*@#%!&]{8,}$")


class AuthorizeResponse(BaseModel):
    user: UserResponse
    access_token: str
    refresh_token: str

from pydantic import BaseModel, EmailStr, conint


class Settings(BaseModel):
    username: EmailStr = "user@example.com"
    password: str = "P@ssw0rd"
    host: str = "smtp.gmail.com"
    port: conint(ge=1, le=65535) = 587
    start_tls: bool = False
    tls: bool = False

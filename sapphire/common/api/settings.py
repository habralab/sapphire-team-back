from pydantic import AnyHttpUrl, BaseModel, conint


class BaseAPISettings(BaseModel):
    port: conint(ge=1, le=65535) = 8000
    root_url: AnyHttpUrl = AnyHttpUrl("http://localhost:8000")
    root_path: str = ""
    allowed_origins: list[str] = []

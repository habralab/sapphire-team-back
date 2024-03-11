from pydantic import AnyHttpUrl, BaseModel, conint


class BaseAPISettings(BaseModel):
    allowed_origins: list[str] = []
    port: conint(ge=1, le=65535) = 8000
    root_path: str = ""
    root_url: AnyHttpUrl = AnyHttpUrl("http://localhost:8000")

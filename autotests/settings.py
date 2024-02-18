import uuid

from pydantic import AnyHttpUrl, AnyUrl
from pydantic_settings import SettingsConfigDict

from sapphire.common.jwt.settings import JWTSettings


class AutotestsSettings(JWTSettings):
    model_config = SettingsConfigDict(extra="allow", env_file=".env", secrets_dir="/run/secrets")

    messenger_base_url: AnyHttpUrl
    notifications_base_url: AnyHttpUrl
    projects_base_url: AnyHttpUrl
    storage_base_url: AnyHttpUrl
    users_base_url: AnyHttpUrl

    messenger_websocket_url: AnyUrl
    notifications_websocket_url: AnyUrl

    oauth2_habr_callback_url: str = ""

    imap_server: str = "imap.gmail.com"
    imap_ssl: bool = True
    imap_starttls: bool = False

    oleg_id: uuid.UUID = uuid.UUID("03fe07b9-109c-4e11-a2a5-184921fbfc49")
    oleg_email: str
    oleg_email_password: str
    matvey_id: uuid.UUID = uuid.UUID("412f1c40-125f-47b9-aaef-1c079c12d63b")
    matvey_email: str
    matvey_email_password: str
    project_id: uuid.UUID = uuid.UUID("cd8bad95-2585-421a-bef8-1ca18353caa6")
    position_id: uuid.UUID = uuid.UUID("035431e1-bcf0-49db-a6bb-6e4c05e99852")
    participant_id: uuid.UUID = uuid.UUID("9b721bc2-e56d-4deb-9359-50bcb1022e74")
    chat_id: uuid.UUID = uuid.UUID("3d6a466a-5165-4299-b2be-86f7d400abd5")
    oleg_notification_id: uuid.UUID = uuid.UUID("c6c293e7-69c8-4f91-a45c-44efd8ea6e79")
    matvey_notification_id: uuid.UUID = uuid.UUID("73c07984-03f2-4dbf-b44c-bc00e3297396")

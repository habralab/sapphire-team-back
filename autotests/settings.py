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

    habr_oauth2_callback_url: str = ""

    imap_server: str = "imap.gmail.com"
    imap_ssl: bool = True
    imap_starttls: bool = False

    oleg_id: uuid.UUID
    oleg_email: str
    oleg_email_password: str
    matvey_id: uuid.UUID
    matvey_email: str
    matvey_email_password: str

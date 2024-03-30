import os
import pathlib
from typing import Type, TypeVar

from pydantic_settings import BaseSettings, SettingsConfigDict

Settings = TypeVar("Settings")


def get_settings(
        settings_cls: Type[Settings],
        env_file: pathlib.Path | None = None,
        env_prefix: str | None = None,
) -> Settings:
    # TODO: Workaround for secrets, fix after pydantic fix  # pylint: disable=fixme
    secrets_dir = pathlib.Path("/run/secrets")
    if secrets_dir.is_dir():
        for secret_file in secrets_dir.iterdir():
            if not secret_file.is_file():
                continue

            os.environ[secret_file.name] = secret_file.read_text().strip()

    return type(
        "Settings",
        (settings_cls, BaseSettings),
        {
            "model_config": SettingsConfigDict(
                env_nested_delimiter="__",
                env_file=None if env_file is None else str(env_file),
                env_prefix=env_prefix or "",
                extra="ignore",
                secrets_dir=str(secrets_dir),
            ),
        },
    )()

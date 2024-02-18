import pathlib
from typing import Type, TypeVar

from pydantic_settings import BaseSettings, SettingsConfigDict


Settings = TypeVar("Settings")


def get_settings(settings_cls: Type[Settings], env_file: pathlib.Path | None = None) -> Settings:
    return type(
        "Settings",
        (settings_cls, BaseSettings),
        {
            "model_config": SettingsConfigDict(
                env_nested_delimiter="__",
                env_file=None if env_file is None else str(env_file),
                extra="ignore",
                secrets_dir="/run/secrets",
            ),
        },
    )()

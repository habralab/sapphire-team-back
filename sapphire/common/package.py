import os
import pathlib
import tomllib

from .functools import get_nested


def get_version() -> str | None:
    path_to_toml_file = pathlib.Path(os.curdir).absolute() / "pyproject.toml"
    with open(path_to_toml_file, "rb") as toml_file:
        pyproject_data = tomllib.load(toml_file)

    version = get_nested(pyproject_data, "tool", "poetry", "version")
    return None if version is None else str(version)

import os
import pathlib
import tomllib
from functools import reduce

from sapphire.common.api.schemas import HealthResponse, ResponseStatus


def get_nested(storage: dict, *keys):
    return reduce(
        lambda value, key: value.get(key, {}) if isinstance(value, dict) else None,
        keys,
        storage,
    )


async def health() -> HealthResponse:
    path_to_toml_file = pathlib.Path(os.curdir).absolute() / "pyproject.toml"
    with open(path_to_toml_file, "rb") as toml_file:
        pyproject_data = tomllib.load(toml_file)

    return HealthResponse(
        status=ResponseStatus.OK,
        version=get_nested(pyproject_data, "tool", "poetry", "version"),
        name="users",
    )

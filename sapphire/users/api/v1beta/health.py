import os
import pathlib
import tomllib

from sapphire.common.api.schemas import HealthResponse, ResponseStatus
from sapphire.common.functions import get_nested


async def health() -> HealthResponse:
    path_to_toml_file = pathlib.Path(os.curdir).absolute() / "pyproject.toml"
    with open(path_to_toml_file, "rb") as toml_file:
        pyproject_data = tomllib.load(toml_file)

    return HealthResponse(
        status=ResponseStatus.OK,
        version=get_nested(pyproject_data, "tool", "poetry", "version"),
        name="users",
    )

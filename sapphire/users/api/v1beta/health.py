import os
import pathlib
import tomllib

from sapphire.common.api.schemas import HealthResponse, ResponseStatus


async def health() -> HealthResponse:
    path_to_toml_file = pathlib.Path(os.curdir).absolute() / "pyproject.toml"
    with open(path_to_toml_file, "rb") as toml_file:
        pyproject_data = tomllib.load(toml_file)

    return HealthResponse(
        status=ResponseStatus.OK,
        version=pyproject_data["tool"]["poetry"]["version"],
        name="users",
    )

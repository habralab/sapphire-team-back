import tomllib
import pathlib
import os

from sapphire.common.api.schemas import HealthResponse, ServiceName


async def health() -> HealthResponse:
    path_to_toml_file = pathlib.Path(os.curdir).absolute() / "pyproject.toml"
    with open(path_to_toml_file, "rb") as toml_file:
        pyproject_data = tomllib.load(toml_file)

    return HealthResponse(version=pyproject_data.get("tool").get("poetry").get("version"), name=ServiceName.USERS)

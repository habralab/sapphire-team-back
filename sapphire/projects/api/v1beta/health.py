import tomllib


async def health():
    with open("pyproject.toml", "rb") as pyproject_file:
        pyproject_data = tomllib.load(pyproject_file)  # pylint: disable=unused-variable

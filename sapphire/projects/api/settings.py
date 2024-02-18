import pathlib

from pydantic import PositiveInt, conint

from sapphire.common.api.settings import BaseAPISettings


class Settings(BaseAPISettings):
    port: conint(ge=1, le=65535) = 8020

    media_dir_path: pathlib.Path = pathlib.Path("/media")
    load_file_chunk_size: PositiveInt = 1024 * 1024 # 1 Mb

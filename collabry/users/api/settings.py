import pathlib

from pydantic import PositiveInt

from collabry.common.api.settings import BaseAPISettings


class Settings(BaseAPISettings):
    media_dir_path: pathlib.Path = pathlib.Path("/media")
    load_file_chunk_size: PositiveInt = 1024 * 1024  # 1 Mb

    oauth2_habr_callback_url: str = ""

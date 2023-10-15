import pathlib
import uuid

import aiofiles
import aiofiles.os
import fastapi
from fastapi.responses import FileResponse

from sapphire.common.jwt.dependencies.rest import auth_user_id, get_request_user_id
from sapphire.users.api.schemas.users import UserFullResponse, UserResponse, UserUpdateRequest
from sapphire.users.database.models import User
from sapphire.users.database.service import UsersDatabaseService

from .dependencies import get_path_user


async def get_user(
        request_user_id: uuid.UUID | None = fastapi.Depends(get_request_user_id),
        path_user: User = fastapi.Depends(get_path_user),
) -> UserResponse | UserFullResponse:
    model_cls = UserResponse if request_user_id != path_user.id else UserFullResponse

    return model_cls.from_db_model(path_user)


async def update_user(
        request: fastapi.Request,
        request_user_id: uuid.UUID = fastapi.Depends(auth_user_id),
        user: User = fastapi.Depends(get_user),
        data: UserUpdateRequest = fastapi.Body(embed=False),
) -> UserFullResponse:
    if user.id != request_user_id:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_403_FORBIDDEN,
            detail="Forbidden.",
        )

    database_service: UsersDatabaseService = request.app.service.database
    async with database_service.transaction() as session:
        user = await database_service.update_user(
            user=user,
            session=session,
            first_name=data.first_name,
            last_name=data.last_name,
        )

    return UserFullResponse.from_db_model(user)


async def get_user_avatar(user: User = fastapi.Depends(get_path_user)) -> FileResponse:
    if user.avatar is None:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_404_NOT_FOUND,
            detail="Avatar not found.",
        )

    return FileResponse(user.avatar)


async def upload_user_avatar(
        request: fastapi.Request,
        request_user_id: uuid.UUID = fastapi.Depends(auth_user_id),
        user: User = fastapi.Depends(get_path_user),
        avatar: fastapi.UploadFile = fastapi.File(...),
) -> UserFullResponse:
    if request_user_id != user.id:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_403_FORBIDDEN,
            detail="Forbidden.",
        )

    database_service: UsersDatabaseService = request.app.service.database
    media_dir_path: pathlib.Path = request.app.service.media_dir_path
    load_file_chunk_size: int = request.app.service.load_file_chunk_size

    avatars_dir_path: pathlib.Path = media_dir_path / "avatars"
    avatar_file_path = avatars_dir_path / f"user-{user.id}"

    await aiofiles.os.makedirs(avatars_dir_path, exist_ok=True)
    async with aiofiles.open(avatar_file_path, "wb") as avatar_file:
        while content := await avatar.read(size=load_file_chunk_size):
            await avatar_file.write(content)

    async with database_service.transaction() as session:
        user = await database_service.update_user_avatar(
            session=session,
            user=user,
            avatar_path=avatar_file_path,
        )

    return UserFullResponse.from_db_model(user=user)

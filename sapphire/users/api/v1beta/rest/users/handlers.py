import pathlib
import uuid

import aiofiles
import aiofiles.os
import fastapi
from fastapi.responses import FileResponse

from sapphire.common.jwt.dependencies.rest import auth_user_id, get_request_user_id
from sapphire.users.database.models import User
from sapphire.users.database.service import UsersDatabaseService

from .dependencies import get_path_user
from .schemas import UserResponse, UserUpdateRequest


async def get_user(
        request_user_id: uuid.UUID | None = fastapi.Depends(get_request_user_id),
        path_user: User = fastapi.Depends(get_path_user),
) -> UserResponse:
    with_email = request_user_id == path_user.id

    return UserResponse.from_db_model(path_user, with_email=with_email)


async def update_user(
        request: fastapi.Request,
        request_user_id: uuid.UUID = fastapi.Depends(auth_user_id),
        user: User = fastapi.Depends(get_path_user),
        data: UserUpdateRequest = fastapi.Body(embed=False),
) -> UserResponse:
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
            main_specialization_id=data.main_specialization_id,
            secondary_specialization_id=data.secondary_specialization_id
        )

    return UserResponse.from_db_model(user)


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
) -> UserResponse:
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
        user = await database_service.update_user(
            session=session,
            user=user,
            avatar=str(avatar_file_path),
        )

    return UserResponse.from_db_model(user=user)


async def delete_user_avatar(
        request: fastapi.Request,
        request_user_id: uuid.UUID = fastapi.Depends(auth_user_id),
        user: User = fastapi.Depends(get_path_user),
) -> UserResponse:
    if request_user_id != user.id:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_403_FORBIDDEN,
            detail="Forbidden.",
        )
    if user.avatar is not None:
        database_service: UsersDatabaseService = request.app.service.database
        original_avatar_file_path = user.avatar
        async with database_service.transaction() as session:
            user = await database_service.update_user(
                session=session,
                user=user,
                avatar=None,
            )

        await aiofiles.os.remove(original_avatar_file_path)

    return UserResponse.from_db_model(user=user)

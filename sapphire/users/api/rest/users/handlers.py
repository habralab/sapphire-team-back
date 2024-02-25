import pathlib
import uuid

import aiofiles
import aiofiles.os
import fastapi
from fastapi.responses import FileResponse

from sapphire.common.api.exceptions import HTTPForbidden
from sapphire.common.jwt.dependencies.rest import get_jwt_data, is_auth
from sapphire.common.jwt.models import JWTData
from sapphire.users import database
from sapphire.users.api.rest.dependencies import update_jwt
from sapphire.users.api.rest.schemas import UserResponse
from sapphire.users.database.models import User

from .dependencies import get_path_user
from .schemas import UserUpdateRequest


async def get_user(
        jwt_data: JWTData | None = fastapi.Depends(get_jwt_data),
        user: User = fastapi.Depends(get_path_user),
) -> UserResponse:
    with_email = jwt_data is not None and jwt_data.user_id == user.id

    return UserResponse.from_db_model(user, with_email=with_email)


async def update_user(
        request: fastapi.Request,
        response: fastapi.Response,
        jwt_data: JWTData = fastapi.Depends(is_auth),
        user: User = fastapi.Depends(get_path_user),
        data: UserUpdateRequest = fastapi.Body(embed=False),
) -> UserResponse:
    if user.id != jwt_data.user_id:
        raise HTTPForbidden()

    database_service: database.Service = request.app.service.database
    async with database_service.transaction() as session:
        user = await database_service.update_user(
            user=user,
            session=session,
            first_name=data.first_name,
            last_name=data.last_name,
            about=data.about,
            main_specialization_id=data.main_specialization_id,
            secondary_specialization_id=data.secondary_specialization_id
        )
        if not user.is_activated:
            user.activate()
            await update_jwt(request=request, response=response, jwt_data=jwt_data, user=user)

    return UserResponse.from_db_model(user)


async def get_user_avatar(user: User = fastapi.Depends(get_path_user)) -> FileResponse:
    if user.avatar is None:
        return None

    return FileResponse(user.avatar)


async def upload_user_avatar(
        request: fastapi.Request,
        jwt_data: JWTData = fastapi.Depends(is_auth),
        user: User = fastapi.Depends(get_path_user),
        avatar: fastapi.UploadFile = fastapi.File(...),
) -> UserResponse:
    if jwt_data.user_id != user.id:
        raise HTTPForbidden()

    database_service: database.Service = request.app.service.database
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
        jwt_data: JWTData = fastapi.Depends(is_auth),
        user: User = fastapi.Depends(get_path_user),
) -> UserResponse:
    if jwt_data.user_id != user.id:
        raise HTTPForbidden()

    if user.avatar is not None:
        database_service: database.Service = request.app.service.database
        original_avatar_file_path = user.avatar
        async with database_service.transaction() as session:
            user = await database_service.update_user(
                session=session,
                user=user,
                avatar=None,
            )

        await aiofiles.os.remove(original_avatar_file_path)

    return UserResponse.from_db_model(user=user)


async def get_user_skills(
        request: fastapi.Request,
        user: User = fastapi.Depends(get_path_user),
) -> set[uuid.UUID]:
    database_service: database.Service = request.app.service.database
    async with database_service.transaction() as session:
        skills = await database_service.get_user_skills(
            session=session,
            user=user,
        )

    return skills


async def update_user_skills(
        request: fastapi.Request,
        jwt_data: JWTData = fastapi.Depends(is_auth),
        user: User = fastapi.Depends(get_path_user),
        data: set[uuid.UUID] = fastapi.Body(embed=False),
) -> set[uuid.UUID]:
    if user.id != jwt_data.user_id:
        raise HTTPForbidden()

    database_service: database.Service = request.app.service.database
    async with database_service.transaction() as session:
        skills = await database_service.update_user_skills(
            session=session,
            user=user,
            skills=data,
        )
    return skills

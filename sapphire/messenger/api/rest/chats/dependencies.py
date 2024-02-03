import uuid

import fastapi

from sapphire.common.api.exceptions import HTTPForbidden, HTTPNotFound
from sapphire.common.jwt.dependencies.rest import is_auth
from sapphire.common.jwt.models import JWTData
from sapphire.messenger import database
from sapphire.messenger.database.models import Chat


async def get_path_chat(
        request: fastapi.Request,
        chat_id: uuid.UUID = fastapi.Path(),
) -> Chat:
    database_service: database.Service = request.app.service.database

    async with database_service.transaction() as session:
        db_chat = await database_service.get_chat(session=session, chat_id=chat_id)
    if db_chat is None:
        raise HTTPNotFound()

    return db_chat


async def path_chat_is_member(
        jwt_data: JWTData = fastapi.Depends(is_auth),
        chat: Chat = fastapi.Depends(get_path_chat),
) -> Chat:
    if jwt_data.user_id not in {member.user_id for member in chat.members}:
        raise HTTPForbidden()

    return chat

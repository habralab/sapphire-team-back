import uuid

import fastapi

from collabry.common.api.exceptions import HTTPForbidden, HTTPNotFound
from collabry.common.jwt.dependencies.rest import is_auth
from collabry.common.jwt.models import JWTData
from collabry.database.models import Chat, ChatMember
from collabry.messenger import database


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
) -> ChatMember:
    for member in chat.members:
        if member.user_id == jwt_data.user_id:
            return member
    raise HTTPForbidden()

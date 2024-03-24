import secrets

import fastapi

from sapphire.users import database


async def check_email(
        request: fastapi.Request,
        email: str
):
    database_service: database.Service = request.app.service.database
    async with database_service.transaction() as session:
        user = await database_service.get_user_email(
            session=session,
            email=email
        )
        if user:
            secret_code = secrets.token_urlsafe(12)

import uuid

import fastapi

from sapphire.projects.database.service import ProjectsDatabaseService

from .schemas import UserStatisticResponse


async def get_user_statistic(
        request: fastapi.Request,
        user_id: uuid.UUID = fastapi.Path(),
) -> UserStatisticResponse:
    database_service: ProjectsDatabaseService = request.app.service.database

    async with database_service.transaction() as session:
        statistic = await database_service.get_user_statistic(session=session, user_id=user_id)

    return UserStatisticResponse.model_validate(statistic)

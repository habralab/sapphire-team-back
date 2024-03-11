import uuid

import fastapi

from sapphire.common.api.exceptions import HTTPForbidden, HTTPNotFound
from sapphire.common.jwt.dependencies.rest import is_auth
from sapphire.common.jwt.models import JWTData
from sapphire.database.models import Project
from sapphire.projects import database


async def get_path_project(
        request: fastapi.Request,
        project_id: uuid.UUID = fastapi.Path(),
) -> Project:
    database_service: database.Service = request.app.service.database

    async with database_service.transaction() as session:
        db_project = await database_service.get_project(session=session, project_id=project_id)
    if db_project is None:
        raise HTTPNotFound()

    return db_project


async def path_project_is_owner(
        jwt_data: JWTData = fastapi.Depends(is_auth),
        project: Project = fastapi.Depends(get_path_project),
) -> Project:
    if project.owner_id != jwt_data.user_id:
        raise HTTPForbidden()

    return project

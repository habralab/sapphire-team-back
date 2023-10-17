import fastapi

from sapphire.projects.api.v1beta.rest.projects.dependencies import path_project_is_owner
from sapphire.projects.database.models import Position, Project
from sapphire.projects.database.service import ProjectsDatabaseService

from .dependencies import get_path_project_position
from .schemas import CreateProjectPositionRequest, ProjectPositionResponse


async def create_project_position(
        request: fastapi.Request,
        project: Project = fastapi.Depends(path_project_is_owner),
        data: CreateProjectPositionRequest = fastapi.Body(embed=False),
) -> ProjectPositionResponse:
    database_service: ProjectsDatabaseService = request.app.service.database

    async with database_service.transaction() as session:
        db_position = await database_service.create_project_position(
            session=session,
            project=project,
            name=data.name,
        )

    return ProjectPositionResponse.model_validate(db_position)


async def remove_project_position(
        request: fastapi.Request,
        project: Project = fastapi.Depends(path_project_is_owner),
        position: Position = fastapi.Depends(get_path_project_position),
) -> ProjectPositionResponse:
    database_service: ProjectsDatabaseService = request.app.service.database

    async with database_service.transaction() as session:
        position = await database_service.remove_project_position(
            session=session,
            position=position,
        )

    return ProjectPositionResponse.model_validate(position)

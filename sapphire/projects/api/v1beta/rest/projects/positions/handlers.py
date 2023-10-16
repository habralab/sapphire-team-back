import fastapi

from sapphire.projects.api.v1beta.rest.projects.dependencies import auth_path_project
from sapphire.projects.database.models import Project
from sapphire.projects.database.service import ProjectsDatabaseService

from .schemas import CreateProjectPositionRequest, ProjectPositionResponse


async def create_project_position(
        request: fastapi.Request,
        project: Project = fastapi.Depends(auth_path_project),
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

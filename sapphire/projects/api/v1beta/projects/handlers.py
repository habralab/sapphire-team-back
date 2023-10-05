import fastapi

from sapphire.projects.database.service import ProjectsDatabaseService

from .schemas import CreateProjectRequest, ProjectResponse


# TODO: Add getting user_id depends
async def create(
    request: fastapi.Request,
    project: CreateProjectRequest = fastapi.Body(embed=True),
) -> ProjectResponse:
    database_service: ProjectsDatabaseService = request.app.service.database
    # TODO: Check that owner_id and user_id the same

    async with database_service.transaction() as session:
        project_db = await database_service.create_project(
            session=session,
            name=project.name,
            owner_id=project.owner_id,
            description=project.description,
            deadline=project.deadline,
        )

    return ProjectResponse.model_validate(project_db)

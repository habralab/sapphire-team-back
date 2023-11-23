import pathlib
import uuid
from datetime import datetime
from typing import Set, Type

from pydantic import BaseModel, NonNegativeInt, confloat, conint
from sqlalchemy import delete, desc, distinct, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from sapphire.common.database.service import BaseDatabaseService
from sapphire.common.utils.empty import Empty
from sapphire.projects.settings import ProjectsSettings

from .models import (
    Base,
    Participant,
    ParticipantStatusEnum,
    Position,
    PositionSkill,
    Project,
    ProjectHistory,
    ProjectStatusEnum,
    Review,
)


class UserStatistic(BaseModel):
    ownership_projects_count: NonNegativeInt
    participant_projects_count: NonNegativeInt
    rate: confloat(ge=1, le=5)


class ProjectsDatabaseService(BaseDatabaseService):
    def get_alembic_config_path(self) -> pathlib.Path:
        return pathlib.Path(__file__).parent / "migrations"

    def get_fixtures_directory_path(self) -> pathlib.Path:
        return pathlib.Path(__file__).parent / "fixtures"

    def get_models(self) -> list[Type[Base]]:
        return [Participant, Position, Project, ProjectHistory, Review]

    async def create_project(
            self,
            session: AsyncSession,
            name: str,
            owner_id: uuid.UUID,
            startline: datetime,
            description: str | None = None,
            deadline: datetime | None = None,
    ) -> Project:
        nested_session = await session.begin_nested()
        project = Project(
            name=name,
            owner_id=owner_id,
            description=description,
            startline=startline,
            deadline=deadline,
        )
        history = ProjectHistory(project=project, status=ProjectStatusEnum.PREPARATION)
        project.history.append(history)
        session.add(project)
        await nested_session.commit()

        await session.refresh(project)

        return project

    async def get_project(
            self,
            session: AsyncSession,
            project_id: uuid.UUID | Type[Empty] = Empty,
    ) -> Project | None:
        filters = []
        if project_id is not Empty:
            filters.append(Project.id == project_id)

        statement = select(Project).where(*filters)
        result = await session.execute(statement)

        return result.unique().scalar_one_or_none()

    async def update_project(
            self,
            session: AsyncSession,
            project: Project,
            name: str | None | Type[Empty] = Empty,
            owner_id: uuid.UUID | None | Type[Empty] = Empty,
            description: str | None | Type[Empty] = Empty,
            startline: datetime | Type[Empty] = Empty,
            deadline: datetime | None | Type[Empty] = Empty,
            avatar: str | None | Type[Empty] = Empty,
            status: ProjectStatusEnum | None | Type[Empty] = Empty,
    ) -> Project:
        query = select(Project).where(Project.id == project.id)
        result = await session.execute(query)
        project = result.unique().scalar_one()

        if name is not Empty:
            project.name = name
        if owner_id is not Empty:
            project.owner_id = owner_id
        if description is not Empty:
            project.description = description
        if deadline is not Empty:
            project.deadline = deadline
        if startline is not Empty:
            project.startline = startline
        if avatar is not Empty:
            project.avatar = avatar
        if status is not Empty:
            project = await self._change_project_status(
                session=session, project=project, status=status,
            )

        session.add(project)

        return project

    async def _change_project_status(
            self,
            session: AsyncSession,
            project: Project,
            status: ProjectStatusEnum,
    ) -> Project:
        nested_session = await session.begin_nested()
        new_history_entry = ProjectHistory(
            project_id=project.id,
            status=status,
        )
        session.add(new_history_entry)
        project.history.insert(0, new_history_entry)
        await nested_session.commit()

        await session.refresh(project)
        return project

    async def get_positions(
            self,
            session: AsyncSession,
            project_id: uuid.UUID | Type[Empty] = Empty,
            is_closed: bool | Type[Empty] = Empty,
            specialization_ids: list[uuid.UUID] | Type[Empty] = Empty,
            skill_ids: list[uuid.UUID] | Type[Empty] = Empty,
            project_query_text: str | Type[Empty] = Empty,
            project_startline_ge: datetime | Type[Empty] = Empty,
            project_startline_le: datetime | Type[Empty] = Empty,
            project_deadline_ge: datetime | Type[Empty] = Empty,
            project_deadline_le: datetime | Type[Empty] = Empty,
            project_status: ProjectStatusEnum | Type[Empty] = Empty,
            page: int = 1,
            per_page: int = 10,
    ) -> list[Position]:
        filters = []
        skill_filters = []
        project_filters = []

        if project_id is not Empty:
            filters.append(Position.project_id == project_id)
        if is_closed is not Empty:
            filters.append(
                Position.closed_at is not None
                if is_closed else
                Position.closed_at is None
            )
        if specialization_ids is not Empty:
            filters.append(Position.specialization_id.in_(specialization_ids))

        if skill_ids is not Empty:
            skill_filters.append(PositionSkill.skill_id.in_(skill_ids))

        if project_query_text is not Empty:
            project_filters.append(or_(
                Project.name.contains(project_query_text),
                Project.description.contains(project_query_text),
            ))
        if project_startline_ge is not Empty:
            project_filters.append(Project.startline >= project_startline_ge)
        if project_startline_le is not Empty:
            project_filters.append(Project.startline <= project_startline_le)
        if project_deadline_ge is not Empty:
            project_filters.append(Project.deadline >= project_deadline_ge)
        if project_deadline_le is not Empty:
            project_filters.append(Project.deadline <= project_deadline_le)
        if project_status is not Empty:
            history_query = (
                select(ProjectHistory)
                .distinct(ProjectHistory.project_id)
                .order_by(ProjectHistory.project_id, desc(ProjectHistory.created_at))
                .subquery()
            )
            project_filters.extend([
                Project.id == history_query.c.project_id,
                project_status == history_query.c.status,
            ])

        if skill_filters:
            filters.append(
                Position.id.in_(select(PositionSkill.position_id).where(*skill_filters))
            )
        if project_filters:
            filters.append(
                Position.project_id.in_(select(Project.id).where(*project_filters))
            )

        statement = select(Position).where(*filters)
        result = await session.execute(statement)
        return list(result.unique().scalars().all())

    async def get_position(
            self,
            session: AsyncSession,
            project_id: uuid.UUID | Type[Empty] = Empty,
            position_id: uuid.UUID | Type[Empty] = Empty,
    ) -> Position | None:
        filters = []
        if project_id is not Empty:
            filters.append(Position.project_id == project_id)
        if position_id is not Empty:
            filters.append(Position.id == position_id)

        statement = select(Position).where(*filters)
        result = await session.execute(statement)

        return result.unique().scalar_one_or_none()

    async def create_position(
            self,
            session: AsyncSession,
            project: Project,
            specialization_id: uuid.UUID,
    ) -> Position:
        position = Position(project=project, specialization_id=specialization_id, skills=[])

        session.add(position)

        return position

    async def remove_position(self, session: AsyncSession, position: Position) -> Position:
        position.closed_at = datetime.utcnow()

        session.add(position)

        return position

    async def update_position_skills(
            self,
            session: AsyncSession,
            position: Position,
            skills: Set[uuid.UUID] = frozenset(),
    ):
        stmt = delete(PositionSkill).where(PositionSkill.position_id == position.id)
        await session.execute(stmt)

        new_skills = [PositionSkill(position=position, skill_id=skill_id) for skill_id in skills]
        position.skills = new_skills

        session.add(position)
        return skills

    async def get_participant(
            self,
            session: AsyncSession,
            participant_id: uuid.UUID | Type[Empty] = Empty,
            position_id: uuid.UUID | Type[Empty] = Empty,
            user_id: uuid.UUID | Type[Empty] = Empty,
    ) -> Participant | None:
        filters = []
        if participant_id is not Empty:
            filters.append(Participant.id == participant_id)
        if position_id is not Empty:
            filters.append(Participant.position_id == position_id)
        if user_id is not Empty:
            filters.append(Participant.user_id == user_id)
        stmt = (
            select(Participant).where(*filters).order_by(Participant.created_at.desc())
        )
        result = await session.execute(stmt)
        return result.scalars().first()

    async def get_participants(
            self,
            session: AsyncSession,
            position: Position | Type[Empty] = Empty,
            user_id: uuid.UUID | Type[Empty] = Empty,
            project_id: uuid.UUID | Type[Empty] = Empty,
    ) -> list[Participant]:
        filters = []
        if position is not Empty:
            filters.append(Participant.position_id == position.id)
        if user_id is not Empty:
            filters.append(Participant.user_id == user_id)
        if project_id is not Empty:
            position_query = select(Position.id).where(Position.project_id == project_id)
            filters.append(Participant.position_id.in_(position_query))
        query = select(Participant).where(*filters)
        result = await session.execute(query)
        return list(result.unique().scalars().all())

    async def create_participant(
            self,
            session: AsyncSession,
            position_id: uuid.UUID,
            user_id: uuid.UUID,
    ) -> Participant:
        participant = Participant(
            user_id=user_id,
            position_id=position_id,
            status=ParticipantStatusEnum.REQUEST,
        )
        session.add(participant)

        return participant

    async def update_participant_status(
            self,
            session: AsyncSession,
            participant: Participant,
            status: ParticipantStatusEnum,
    ) -> Participant:
        participant.status = status
        if status == ParticipantStatusEnum.JOINED:
            participant.joined_at = datetime.utcnow()
        session.add(participant)

        return participant

    async def get_projects(
        self,
        session: AsyncSession,
        query_text: str | Type[Empty] = Empty,
        owner_id: uuid.UUID | Type[Empty] = Empty,
        user_id: uuid.UUID | Type[Empty] = Empty,
        startline_le: datetime | Type[Empty] = Empty,
        startline_ge: datetime | Type[Empty] = Empty,
        deadline_le: datetime | Type[Empty] = Empty,
        deadline_ge: datetime | Type[Empty] = Empty,
        status: ProjectStatusEnum | Type[Empty] = Empty,
        position_skill_ids: list[uuid.UUID] | Type[Empty] = Empty,
        position_specialization_ids: list[uuid.UUID] | Type[Empty] = Empty,
        participant_user_ids: list[uuid.UUID] | Type[Empty] = Empty,
        page: int = 1,
        per_page: int = 10,
    ) -> list[Project]:
        filters = []
        position_filters = []
        participant_filters = []
        query = select(Project).order_by(Project.created_at.desc())

        if query_text is not Empty:
            filters.append(
                or_(
                    Project.name.contains(query_text),
                    Project.description.contains(query_text),
                )
            )
        if owner_id is not Empty:
            filters.append(Project.owner_id == owner_id)
        if user_id is not Empty:
            filters.append(or_(
                Project.owner_id == owner_id,
                Project.id.in_(select(Position.project_id).where(
                    Position.id.in_(select(Participant.position_id).where(
                        Participant.user_id == user_id,
                    )),
                )),
            ))
        if startline_le is not Empty:
            filters.append(Project.startline <= startline_le)
        if startline_ge is not Empty:
            filters.append(Project.startline >= startline_ge)
        if deadline_le is not Empty:
            filters.append(Project.deadline <= deadline_le)
        if deadline_ge is not Empty:
            filters.append(Project.deadline >= deadline_ge)
        if status is not Empty:
            history_query = (
                select(ProjectHistory)
                .distinct(ProjectHistory.project_id)
                .order_by(ProjectHistory.project_id, desc(ProjectHistory.created_at))
                .subquery()
            )
            filters.extend([
                Project.id == history_query.c.project_id,
                status == history_query.c.status,
            ])

        if position_specialization_ids is not Empty:
            position_filters.append(
                Position.specialization_id.in_(position_specialization_ids)
            )
        if position_skill_ids is not Empty:
            position_skill_query = (
                select(PositionSkill.position_id)
                .where(PositionSkill.skill_id.in_(position_skill_ids))
            )
            position_filters.append(Position.id.in_(position_skill_query))
        if participant_user_ids is not Empty:
            participant_filters.append(Participant.user_id.in_(participant_user_ids))

        if participant_filters:
            position_filters.append(
                Position.id.in_(select(Participant.position_id).where(*participant_filters))
            )
        if position_filters:
            filters.append(
                Project.id.in_(select(Position.project_id).where(*position_filters))
            )

        query = query.where(*filters)

        offset = (page - 1) * per_page
        query = query.limit(per_page).offset(offset)

        result = await session.execute(query)

        return list(result.unique().scalars().all())

    async def get_user_statistic(self, session: AsyncSession, user_id: uuid.UUID) -> UserStatistic:
        stmt = select(
            func.count(Project.id),  # pylint: disable=not-callable
        ).where(Project.owner_id == user_id)
        result = await session.execute(stmt)
        ownership_projects_count = result.scalar_one()

        stmt_position_ids = (
            select(Participant.position_id)
            .where(
                Participant.user_id == user_id, Participant.status == ParticipantStatusEnum.JOINED
            )
        )
        stmt = (
            select(func.count(distinct(Position.project_id)))  # pylint: disable=not-callable
            .where(Position.id.in_(stmt_position_ids))
        )
        result = await session.execute(stmt)
        participant_projects_count = result.scalar_one()

        rate = 5.0

        return UserStatistic(
            ownership_projects_count=ownership_projects_count,
            participant_projects_count=participant_projects_count,
            rate=rate,
        )

    async def create_review(
            self,
            session: AsyncSession,
            project: Project,
            from_user_id: uuid.UUID,
            to_user_id: uuid.UUID,
            rate: conint(ge=1, le=5),
            text: str,
    ) -> Review:
        review = Review(
            project_id=project.id,
            from_user_id=from_user_id,
            to_user_id=to_user_id,
            rate=rate,
            text=text,
        )

        session.add(review)
        return review

    async def get_review(
            self,
            session: AsyncSession,
            project: Project | Type[Empty] = Empty,
            from_user_id: uuid.UUID | Type[Empty] = Empty,
            to_user_id: uuid.UUID | Type[Empty] = Empty,
    ) -> Review | None:
        filters = []

        if project is not Empty:
            filters.append(Review.project_id == project.id)
        if from_user_id is not Empty:
            filters.append(Review.from_user_id == from_user_id)
        if to_user_id is not Empty:
            filters.append(Review.to_user_id == to_user_id)

        query = select(Review).where(*filters)
        result = await session.execute(query)

        return result.unique().scalar_one_or_none()


def get_service(settings: ProjectsSettings) -> ProjectsDatabaseService:
    return ProjectsDatabaseService(dsn=str(settings.db_dsn))

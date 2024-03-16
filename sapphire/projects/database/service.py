import uuid
from datetime import datetime, timezone
from typing import Set, Type

from pydantic import BaseModel, NonNegativeInt, confloat, conint
from sqlalchemy import desc, distinct, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from sapphire.common.database.service import BaseDatabaseService
from sapphire.common.utils.empty import Empty
from sapphire.database.models import (
    Participant,
    ParticipantStatusEnum,
    Position,
    PositionSkill,
    Project,
    ProjectHistory,
    ProjectStatusEnum,
    Review,
    User,
)

from .settings import Settings


class UserStatistic(BaseModel):
    ownership_projects_count: NonNegativeInt
    participant_projects_count: NonNegativeInt
    rate: confloat(ge=1, le=5)


class Service(BaseDatabaseService):  # pylint: disable=abstract-method
    async def get_user(self, session: AsyncSession, user_id: uuid.UUID) -> User | None:
        statement = select(User).where(User.id == user_id)
        result = await session.execute(statement)

        return result.unique().scalar_one_or_none()

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

    async def _get_positions_filters(
            self,
            project_id: uuid.UUID | Type[Empty] = Empty,
            specialization_ids: list[uuid.UUID] | Type[Empty] = Empty,
            skill_ids: list[uuid.UUID] | Type[Empty] = Empty,
            joined_user_id: uuid.UUID | Type[Empty] = Empty,
            project_query_text: str | Type[Empty] = Empty,
            project_startline_ge: datetime | Type[Empty] = Empty,
            project_startline_le: datetime | Type[Empty] = Empty,
            project_deadline_ge: datetime | Type[Empty] = Empty,
            project_deadline_le: datetime | Type[Empty] = Empty,
            project_statuses: list[ProjectStatusEnum] | Type[Empty] = Empty,
    ) -> list:
        filters = []
        skill_filters = []
        project_filters = []

        if project_id is not Empty:
            filters.append(Position.project_id == project_id)
        if specialization_ids is not Empty:
            filters.append(Position.specialization_id.in_(specialization_ids))

        if skill_ids is not Empty:
            skill_filters.append(PositionSkill.skill_id.in_(skill_ids))

        if joined_user_id is not Empty:
            filters.append(or_(
                Position.project_id.in_(select(Project.id).where(
                    Project.owner_id == joined_user_id,
                )),
                Position.id.in_(select(Participant.position_id).where(
                    Participant.user_id == joined_user_id,
                    Participant.status == ParticipantStatusEnum.JOINED,
                ))
            ))

        if project_query_text is not Empty:
            project_filters.append(or_(
                Project.name.icontains(project_query_text),
                Project.description.icontains(project_query_text),
            ))
        if project_startline_ge is not Empty:
            project_filters.append(Project.startline >= project_startline_ge)
        if project_startline_le is not Empty:
            project_filters.append(Project.startline <= project_startline_le)
        if project_deadline_ge is not Empty:
            project_filters.append(Project.deadline >= project_deadline_ge)
        if project_deadline_le is not Empty:
            project_filters.append(Project.deadline <= project_deadline_le)
        if project_statuses is not Empty:
            history_query = (
                select(ProjectHistory)
                .distinct(ProjectHistory.project_id)
                .order_by(ProjectHistory.project_id, desc(ProjectHistory.created_at))
                .subquery()
            )
            project_filters.extend([
                Project.id == history_query.c.project_id,
                history_query.c.status.in_(project_statuses),
            ])

        if skill_filters:
            filters.append(
                Position.id.in_(select(PositionSkill.position_id).where(*skill_filters))
            )
        if project_filters:
            filters.append(
                Position.project_id.in_(select(Project.id).where(*project_filters))
            )

        return filters

    async def get_positions_count(
            self,
            session: AsyncSession,
            project_id: uuid.UUID | Type[Empty] = Empty,
            specialization_ids: list[uuid.UUID] | Type[Empty] = Empty,
            skill_ids: list[uuid.UUID] | Type[Empty] = Empty,
            joined_user_id: uuid.UUID | Type[Empty] = Empty,
            project_query_text: str | Type[Empty] = Empty,
            project_startline_ge: datetime | Type[Empty] = Empty,
            project_startline_le: datetime | Type[Empty] = Empty,
            project_deadline_ge: datetime | Type[Empty] = Empty,
            project_deadline_le: datetime | Type[Empty] = Empty,
            project_statuses: list[ProjectStatusEnum] | Type[Empty] = Empty,
    ) -> int:
        filters = await self._get_positions_filters(
            project_id=project_id,
            specialization_ids=specialization_ids,
            skill_ids=skill_ids,
            joined_user_id=joined_user_id,
            project_query_text=project_query_text,
            project_startline_ge=project_startline_ge,
            project_startline_le=project_startline_le,
            project_deadline_ge=project_deadline_ge,
            project_deadline_le=project_deadline_le,
            project_statuses=project_statuses,
        )

        statement = select(func.count(Position.id)).where(*filters) # pylint: disable=not-callable
        result = await session.scalar(statement)
        return result

    async def get_positions(
            self,
            session: AsyncSession,
            project_id: uuid.UUID | Type[Empty] = Empty,
            specialization_ids: list[uuid.UUID] | Type[Empty] = Empty,
            skill_ids: list[uuid.UUID] | Type[Empty] = Empty,
            joined_user_id: uuid.UUID | Type[Empty] = Empty,
            project_query_text: str | Type[Empty] = Empty,
            project_startline_ge: datetime | Type[Empty] = Empty,
            project_startline_le: datetime | Type[Empty] = Empty,
            project_deadline_ge: datetime | Type[Empty] = Empty,
            project_deadline_le: datetime | Type[Empty] = Empty,
            project_statuses: list[ProjectStatusEnum] | Type[Empty] = Empty,
            page: int = 1,
            per_page: int = 10,
    ) -> list[Position]:
        filters = await self._get_positions_filters(
            project_id=project_id,
            specialization_ids=specialization_ids,
            skill_ids=skill_ids,
            joined_user_id=joined_user_id,
            project_query_text=project_query_text,
            project_startline_ge=project_startline_ge,
            project_startline_le=project_startline_le,
            project_deadline_ge=project_deadline_ge,
            project_deadline_le=project_deadline_le,
            project_statuses=project_statuses,
        )

        statement = select(Position).where(*filters).order_by(Position.created_at.desc())

        offset = (page - 1) * per_page
        statement = statement.limit(per_page).offset(offset)

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
        position.closed_at = datetime.now(tz=timezone.utc)

        session.add(position)

        return position

    async def update_position_skills(
            self,
            session: AsyncSession,
            position: Position,
            skills: Set[uuid.UUID] = frozenset(),
    ):
        async with session.begin_nested():
            position.skills = []
            session.add(position)

        async with session.begin_nested():
            new_skills = [
                PositionSkill(position=position, skill_id=skill_id)
                for skill_id in skills
            ]
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
            position_id: uuid.UUID | Type[Empty] = Empty,
            user_id: uuid.UUID | Type[Empty] = Empty,
            project_id: uuid.UUID | Type[Empty] = Empty,
            status: ParticipantStatusEnum | Type[Empty] = Empty,
            created_at_le: datetime | Type[Empty] = Empty,
            created_at_ge: datetime | Type[Empty] = Empty,
            joined_at_le: datetime | Type[Empty] = Empty,
            joined_at_ge: datetime | Type[Empty] = Empty,
            updated_at_le: datetime | Type[Empty] = Empty,
            updated_at_ge: datetime | Type[Empty] = Empty,
            page: int = 1,
            per_page: int = 10,
    ) -> list[Participant]:
        filters = await self._get_participants_filters(
            position_id=position_id,
            user_id=user_id,
            project_id=project_id,
            status=status,
            created_at_le=created_at_le,
            created_at_ge=created_at_ge,
            joined_at_le=joined_at_le,
            joined_at_ge=joined_at_ge,
            updated_at_le=updated_at_le,
            updated_at_ge=updated_at_ge,
        )
        query = select(Participant).where(*filters)

        offset = (page - 1) * per_page
        query = query.limit(per_page).offset(offset)

        result = await session.execute(query)
        return list(result.unique().scalars().all())

    async def _get_participants_filters(
        self,
        position_id: uuid.UUID | Type[Empty] = Empty,
        user_id: uuid.UUID | Type[Empty] = Empty,
        project_id: uuid.UUID | Type[Empty] = Empty,
        status: ParticipantStatusEnum | Type[Empty] = Empty,
        created_at_le: datetime | Type[Empty] = Empty,
        created_at_ge: datetime | Type[Empty] = Empty,
        joined_at_le: datetime | Type[Empty] = Empty,
        joined_at_ge: datetime | Type[Empty] = Empty,
        updated_at_le: datetime | Type[Empty] = Empty,
        updated_at_ge: datetime | Type[Empty] = Empty,
    ) -> list:
        filters = []

        if user_id is not Empty:
            filters.append(Participant.user_id == user_id)
        if position_id is not Empty:
            filters.append(Participant.position_id == position_id)
        if project_id is not Empty:
            position_query = select(Position.id).where(Position.project_id == project_id)
            filters.append(Participant.position_id.in_(position_query))
        if status is not Empty:
            filters.append(Participant.status == status)
        if created_at_le is not Empty:
            filters.append(Participant.created_at <= created_at_le)
        if created_at_ge is not Empty:
            filters.append(Participant.created_at >= created_at_ge)
        if joined_at_le is not Empty:
            filters.append(Participant.joined_at <= joined_at_le)
        if joined_at_ge is not Empty:
            filters.append(Participant.joined_at >= joined_at_ge)
        if updated_at_le is not Empty:
            filters.append(Participant.updated_at <= updated_at_le)
        if updated_at_ge is not Empty:
            filters.append(Participant.updated_at >= updated_at_ge)

        return filters

    async def get_participants_count(
        self,
        session: AsyncSession,
        position_id: uuid.UUID | Type[Empty] = Empty,
        user_id: uuid.UUID | Type[Empty] = Empty,
        project_id: uuid.UUID | Type[Empty] = Empty,
        status: ParticipantStatusEnum | Type[Empty] = Empty,
        created_at_le: datetime | Type[Empty] = Empty,
        created_at_ge: datetime | Type[Empty] = Empty,
        joined_at_le: datetime | Type[Empty] = Empty,
        joined_at_ge: datetime | Type[Empty] = Empty,
        updated_at_le: datetime | Type[Empty] = Empty,
        updated_at_ge: datetime | Type[Empty] = Empty,
        page: int = 1,
        per_page: int = 10,
    ) -> int:
        query = select(func.count(Participant.id))  # pylint: disable=not-callable
        filters = await self._get_participants_filters(
            position_id=position_id,
            user_id=user_id,
            project_id=project_id,
            status=status,
            created_at_le=created_at_le,
            created_at_ge=created_at_ge,
            joined_at_le=joined_at_le,
            joined_at_ge=joined_at_ge,
            updated_at_le=updated_at_le,
            updated_at_ge=updated_at_ge,
        )
        query = query.where(*filters)

        result = await session.scalar(query)
        return result

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
            participant.joined_at = datetime.now(tz=timezone.utc)
        session.add(participant)

        return participant

    async def _get_projects_filters(
            self,
            query_text: str | Type[Empty] = Empty,
            owner_id: uuid.UUID | Type[Empty] = Empty,
            user_id: uuid.UUID | Type[Empty] = Empty,
            startline_le: datetime | Type[Empty] = Empty,
            startline_ge: datetime | Type[Empty] = Empty,
            deadline_le: datetime | Type[Empty] = Empty,
            deadline_ge: datetime | Type[Empty] = Empty,
            statuses: list[ProjectStatusEnum] | Type[Empty] = Empty,
            position_skill_ids: list[uuid.UUID] | Type[Empty] = Empty,
            position_specialization_ids: list[uuid.UUID] | Type[Empty] = Empty,
            participant_user_ids: list[uuid.UUID] | Type[Empty] = Empty,
    ) -> list:
        filters = []
        position_filters = []
        participant_filters = []

        if query_text is not Empty:
            filters.append(
                or_(
                    Project.name.icontains(query_text),
                    Project.description.icontains(query_text),
                )
            )
        if owner_id is not Empty:
            filters.append(Project.owner_id == owner_id)
        if user_id is not Empty:
            filters.append(or_(
                Project.owner_id == user_id,
                Project.id.in_(select(Position.project_id).where(
                    Position.id.in_(select(Participant.position_id).where(
                        Participant.user_id == user_id,
                        Participant.status == ParticipantStatusEnum.JOINED,
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
        if statuses is not Empty:
            history_query = (
                select(ProjectHistory)
                .distinct(ProjectHistory.project_id)
                .order_by(ProjectHistory.project_id, desc(ProjectHistory.created_at))
                .subquery()
            )
            filters.extend([
                Project.id == history_query.c.project_id,
                history_query.c.status.in_(statuses),
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

        return filters

    async def get_projects_count(
        self,
        session: AsyncSession,
        query_text: str | Type[Empty] = Empty,
        owner_id: uuid.UUID | Type[Empty] = Empty,
        user_id: uuid.UUID | Type[Empty] = Empty,
        startline_le: datetime | Type[Empty] = Empty,
        startline_ge: datetime | Type[Empty] = Empty,
        deadline_le: datetime | Type[Empty] = Empty,
        deadline_ge: datetime | Type[Empty] = Empty,
        statuses: list[ProjectStatusEnum] | Type[Empty] = Empty,
        position_skill_ids: list[uuid.UUID] | Type[Empty] = Empty,
        position_specialization_ids: list[uuid.UUID] | Type[Empty] = Empty,
        participant_user_ids: list[uuid.UUID] | Type[Empty] = Empty,
    ) -> int:
        query = select(func.count(Project.id))  # pylint: disable=not-callable
        filters = await self._get_projects_filters(
            query_text=query_text,
            owner_id=owner_id,
            user_id=user_id,
            startline_le=startline_le,
            startline_ge=startline_ge,
            deadline_le=deadline_le,
            deadline_ge=deadline_ge,
            statuses=statuses,
            position_skill_ids=position_skill_ids,
            position_specialization_ids=position_specialization_ids,
            participant_user_ids=participant_user_ids,
        )
        query = query.where(*filters)

        result = await session.scalar(query)
        return result

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
        statuses: list[ProjectStatusEnum] | Type[Empty] = Empty,
        position_skill_ids: list[uuid.UUID] | Type[Empty] = Empty,
        position_specialization_ids: list[uuid.UUID] | Type[Empty] = Empty,
        participant_user_ids: list[uuid.UUID] | Type[Empty] = Empty,
        page: int = 1,
        per_page: int = 10,
    ) -> list[Project]:
        query = select(Project).order_by(Project.created_at.desc())
        filters = await self._get_projects_filters(
            query_text=query_text,
            owner_id=owner_id,
            user_id=user_id,
            startline_le=startline_le,
            startline_ge=startline_ge,
            deadline_le=deadline_le,
            deadline_ge=deadline_ge,
            statuses=statuses,
            position_skill_ids=position_skill_ids,
            position_specialization_ids=position_specialization_ids,
            participant_user_ids=participant_user_ids,
        )
        query = query.where(*filters)

        offset = (page - 1) * per_page
        query = query.limit(per_page).offset(offset)

        result = await session.execute(query)

        return list(result.unique().scalars().all())

    async def get_project_history_count(
        self, session: AsyncSession, project_id: uuid.UUID
    ) -> int:
        query = (
            select(func.count(ProjectHistory.id)).where(ProjectHistory.project_id == project_id) # pylint: disable=not-callable
        )

        result = await session.scalar(query)

        return result

    async def get_project_history(
        self,
        session: AsyncSession,
        project_id: uuid.UUID,
        page: int = 1,
        per_page: int = 10,
    ) -> list[ProjectHistory]:
        query = (
            select(ProjectHistory)
            .where(ProjectHistory.project_id == project_id)
            .order_by(ProjectHistory.created_at.desc())
        )

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


def get_service(settings: Settings) -> Service:
    return Service(dsn=str(settings.dsn))

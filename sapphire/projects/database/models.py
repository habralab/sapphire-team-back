import enum
import uuid
from datetime import datetime

from sqlalchemy import Enum, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class ProjectStatusEnum(str, enum.Enum):
    PREPARATION = "preparation"
    IN_WORK = "in_work"
    FINISHED = "finished"


class ParticipantStatusEnum(str, enum.Enum):
    REQUEST = "request"
    DECLINED = "declined"
    JOINED = "joined"
    LEFT = "left"


class Base(DeclarativeBase):
    pass


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[uuid.UUID] = mapped_column(default=uuid.uuid4, primary_key=True)
    name: Mapped[str]
    description: Mapped[str | None]
    owner_id: Mapped[uuid.UUID]
    deadline: Mapped[datetime | None]
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now, onupdate=datetime.now)
    avatar: Mapped[str | None]

    history: Mapped[list["ProjectHistory"]] = relationship(
        back_populates="project",
        order_by="desc(ProjectHistory.created_at)",
        lazy="joined",
    )
    positions: Mapped[list["Position"]] = relationship(back_populates="project", lazy="joined")
    reviews: Mapped[list["Review"]] = relationship(back_populates="project", lazy="joined")

    @property
    def status(self):
        return self.history[0].status

    @property
    def joined_participants(self) -> list["Participant"]:
        return [
            participant
            for position in self.positions
            for participant in position.participants
            if participant.status == ParticipantStatusEnum.JOINED
        ]


class ProjectHistory(Base):
    __tablename__ = "projects_history"

    id: Mapped[uuid.UUID] = mapped_column(default=uuid.uuid4, primary_key=True)
    project_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("projects.id"), primary_key=True)
    status: Mapped[ProjectStatusEnum] = mapped_column(Enum(ProjectStatusEnum))
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)

    project: Mapped[Project] = relationship(back_populates="history", lazy="joined")


class Position(Base):
    __tablename__ = "project_positions"

    id: Mapped[uuid.UUID] = mapped_column(default=uuid.uuid4, primary_key=True, unique=True)
    project_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("projects.id"), primary_key=True)
    specialization_id: Mapped[uuid.UUID]
    closed_at: Mapped[datetime | None]
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now, onupdate=datetime.now)

    project: Mapped[Project] = relationship(back_populates="positions", lazy="joined")
    participants: Mapped[list["Participant"]] = relationship(back_populates="position",
                                                             lazy="joined")


class PositionsSkills(Base):
    __tablename__ = "project_positions_skills"

    position_id: Mapped[str] = mapped_column(
        ForeignKey("project_positions.id"), primary_key=True
    )
    skill_id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.now, onupdate=datetime.now
    )


class Participant(Base):
    __tablename__ = "project_participants"

    id: Mapped[uuid.UUID] = mapped_column(default=uuid.uuid4, primary_key=True)
    position_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("project_positions.id"),
                                                   primary_key=True)
    user_id: Mapped[uuid.UUID]
    status: Mapped[ParticipantStatusEnum] = mapped_column(Enum(ParticipantStatusEnum))
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now, onupdate=datetime.now)
    joined_at: Mapped[datetime | None]

    position: Mapped[Position] = relationship(back_populates="participants", lazy="joined")
    reviews: Mapped[list["Review"]] = relationship(back_populates="participant", lazy="joined")


class Review(Base):
    __tablename__ = "project_reviews"

    id: Mapped[uuid.UUID] = mapped_column(default=uuid.uuid4, primary_key=True)
    project_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("projects.id"))
    participant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("project_participants.id"))
    from_user_id: Mapped[uuid.UUID]
    to_user_id: Mapped[uuid.UUID]
    rate: Mapped[int]
    text: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now, onupdate=datetime.now)

    participant: Mapped[Participant] = relationship(back_populates="reviews", lazy="joined")
    project: Mapped[Project] = relationship(back_populates="reviews", lazy="joined")

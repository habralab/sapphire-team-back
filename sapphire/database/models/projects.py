import enum
import uuid
from datetime import datetime

from sqlalchemy import Enum, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .storage import Skill, Specialization
from .users import User
from .utils import now


class ProjectStatusEnum(str, enum.Enum):
    PREPARATION = "preparation"
    IN_WORK = "in_work"
    FINISHED = "finished"


class ParticipantStatusEnum(str, enum.Enum):
    REQUEST = "request"
    DECLINED = "declined"
    JOINED = "joined"
    LEFT = "left"


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[uuid.UUID] = mapped_column(default=uuid.uuid4, primary_key=True)

    name: Mapped[str]
    description: Mapped[str | None]
    owner_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    startline: Mapped[datetime]
    deadline: Mapped[datetime | None]
    avatar: Mapped[str | None]

    created_at: Mapped[datetime] = mapped_column(default=now)
    updated_at: Mapped[datetime] = mapped_column(default=now, onupdate=now)

    history: Mapped[list["ProjectHistory"]] = relationship(
        back_populates="project",
        order_by="desc(ProjectHistory.created_at)",
    )
    last_history: Mapped["ProjectHistory"] = relationship(
        back_populates="project",
        order_by="desc(ProjectHistory.created_at)",
        lazy=False,
    )
    positions: Mapped[list["Position"]] = relationship(back_populates="project")
    reviews: Mapped[list["Review"]] = relationship(back_populates="project")
    owner: Mapped[User] = relationship(foreign_keys=[owner_id], lazy=False)

    __table_args__ = (
        Index("projects__owner_id_idx", "owner_id", postgresql_using="hash"),
    )

    @property
    def status(self) -> ProjectStatusEnum:
        return self.last_history.status


class ProjectHistory(Base):
    __tablename__ = "projects_history"

    id: Mapped[uuid.UUID] = mapped_column(default=uuid.uuid4, primary_key=True)

    project_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("projects.id"))
    status: Mapped[ProjectStatusEnum] = mapped_column(Enum(ProjectStatusEnum))

    created_at: Mapped[datetime] = mapped_column(default=now)

    project: Mapped[Project] = relationship(back_populates="history", lazy=False)

    __table_args__ = (
        Index("projects_history__project_id_idx", "project_id", postgresql_using="hash"),
        Index("projects_history__created_at_idx", "created_at", postgresql_using="btree"),
    )


class Position(Base):
    __tablename__ = "positions"

    id: Mapped[uuid.UUID] = mapped_column(default=uuid.uuid4, primary_key=True)

    project_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("projects.id"))
    specialization_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("specializations.id"))

    closed_at: Mapped[datetime | None]
    created_at: Mapped[datetime] = mapped_column(default=now)
    updated_at: Mapped[datetime] = mapped_column(default=now, onupdate=now)

    project: Mapped[Project] = relationship(back_populates="positions", lazy=False)
    specialization: Mapped[Specialization] = relationship(Specialization)
    participants: Mapped[list["Participant"]] = relationship(back_populates="position",
                                                             lazy=False)
    joined_participants: Mapped[list["Participant"]] = relationship(
        back_populates="position",
        primaryjoin=(
            "and_(Position.id == Participant.position_id, "
            f"Participant.status == '{ParticipantStatusEnum.JOINED.value}')"
        ),
        lazy=False,
    )
    skills: Mapped[list["PositionSkill"]] = relationship(back_populates="position", lazy=False,
                                                         cascade="all, delete-orphan")

    __table_args__ = (
        Index("positions__project_id_idx", "project_id", postgresql_using="hash"),
        Index("positions__specialization_id_idx", "specialization_id",
              postgresql_using="hash"),
        Index("positions__created_at_idx", "created_at", postgresql_using="btree"),
    )


class PositionSkill(Base):
    __tablename__ = "positions_skills"

    position_id: Mapped[str] = mapped_column(ForeignKey("positions.id"), primary_key=True)
    skill_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("skills.id"), primary_key=True)

    created_at: Mapped[datetime] = mapped_column(default=now)
    updated_at: Mapped[datetime] = mapped_column(default=now, onupdate=now)

    position: Mapped[Position] = relationship(back_populates="skills", lazy=False)
    skill: Mapped[Skill] = relationship(lazy=False)

    __table_args__ = (
        Index("positions_skills__position_id_idx", "position_id", postgresql_using="hash"),
        Index("positions_skills__skill_id_idx", "skill_id", postgresql_using="hash"),
        Index("positions_skills__created_at_idx", "created_at", postgresql_using="btree"),
    )


class Participant(Base):
    __tablename__ = "participants"

    id: Mapped[uuid.UUID] = mapped_column(default=uuid.uuid4, primary_key=True)

    position_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("positions.id"))
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    status: Mapped[ParticipantStatusEnum] = mapped_column(Enum(ParticipantStatusEnum))

    created_at: Mapped[datetime] = mapped_column(default=now)
    updated_at: Mapped[datetime] = mapped_column(default=now, onupdate=now)
    joined_at: Mapped[datetime | None]

    position: Mapped[Position] = relationship(back_populates="participants", lazy=False)
    user: Mapped[User] = relationship(lazy=False)

    __table_args__ = (
        Index("participants__position_id_idx", "position_id", postgresql_using="hash"),
        Index("participants__user_id_idx", "user_id", postgresql_using="hash"),
    )


class Review(Base):
    __tablename__ = "reviews"

    id: Mapped[uuid.UUID] = mapped_column(default=uuid.uuid4, primary_key=True)

    project_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("projects.id"))
    from_user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    to_user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    rate: Mapped[int]
    text: Mapped[str]

    created_at: Mapped[datetime] = mapped_column(default=now)
    updated_at: Mapped[datetime] = mapped_column(default=now, onupdate=now)

    project: Mapped[Project] = relationship(back_populates="reviews", lazy=False)
    from_user: Mapped[User] = relationship(foreign_keys=[from_user_id], lazy=False)
    to_user: Mapped[User] = relationship(foreign_keys=[to_user_id])

    __table_args__ = (
        Index("reviews__project_id_idx", "project_id", postgresql_using="hash"),
        Index("reviews__from_user_id_idx", "from_user_id", postgresql_using="hash"),
        Index("reviews__to_user_id_idx", "to_user_id", postgresql_using="hash"),
    )

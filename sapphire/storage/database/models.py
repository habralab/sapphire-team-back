import uuid
from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Skill(Base):
    __tablename__ = "skills"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    name: Mapped[str | None]
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)


class Specialization(Base):
    __tablename__ = "specializations"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    name: Mapped[str | None]
    is_other: Mapped[bool] = mapped_column(default=False)
    group_id: Mapped[str | None] = mapped_column(ForeignKey("specialization_groups.id"))
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)


class SpecializationsSkills(Base):
    __tablename__ = "specializations_skills"

    skill_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("skills.id"), primary_key=True)
    specialization_id: Mapped[str] = mapped_column(
        ForeignKey("specializations.id"), primary_key=True
    )
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.now, onupdate=datetime.now
    )


class SpecializationGroup(Base):
    __tablename__ = "specialization_groups"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    name: Mapped[str | None]
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)

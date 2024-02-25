import uuid
from datetime import datetime

from pydantic import PositiveInt
from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from .base import Base


class SpecializationGroup(Base):
    __tablename__ = "specialization_groups"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    habr_id: Mapped[PositiveInt | None] = mapped_column(unique=True)
    name: Mapped[str]
    name_en: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    specializations: Mapped[list["Specialization"]] = relationship(back_populates="group",
                                                                   lazy=False)

class Specialization(Base):
    __tablename__ = "specializations"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    habr_id: Mapped[PositiveInt | None] = mapped_column(unique=True)
    name: Mapped[str]
    name_en: Mapped[str]
    group_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("specialization_groups.id"))
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    group: Mapped[SpecializationGroup] = relationship(back_populates="specializations",
                                                      lazy=False)


class Skill(Base):
    __tablename__ = "skills"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    habr_id: Mapped[PositiveInt | None] = mapped_column(unique=True)
    name: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

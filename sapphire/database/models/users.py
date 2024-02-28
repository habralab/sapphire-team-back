import uuid
from datetime import datetime

from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from .base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(default=uuid.uuid4, primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)
    first_name: Mapped[str | None]
    last_name: Mapped[str | None]
    avatar: Mapped[str | None] = mapped_column(unique=True)
    is_activated: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)

    profile: Mapped["Profile"] = relationship("Profile", back_populates="user", lazy=False)
    skills: Mapped[list["UserSkill"]] = relationship(back_populates="user", lazy=False,
                                                     cascade="all, delete-orphan")

    @property
    def has_avatar(self) -> bool:
        return self.avatar is not None

    def activate(self) -> bool:
        if (self.first_name or "").strip() and (self.last_name or "").strip():
            self.is_activated = True

        return self.is_activated


class Profile(Base):
    __tablename__ = "profiles"

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), primary_key=True)
    about: Mapped[str | None] = mapped_column(Text)
    main_specialization_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("specializations.id"))
    secondary_specialization_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("specializations.id"))
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)

    user: Mapped[User] = relationship(back_populates="profile", lazy=False)
    main_specialization: Mapped["Specialization"] = relationship("Specialization")
    secondary_specialization: Mapped["Specialization"] = relationship("Specialization")


class UserSkill(Base):
    __tablename__ = "user_skills"

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), primary_key=True)
    skill_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("skills.id"), primary_key=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)

    user: Mapped[User] = relationship(back_populates="skills", lazy=False)
    skill: Mapped["Skill"] = relationship(back_populates="users", lazy=False)

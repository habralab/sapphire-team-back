import uuid
from datetime import datetime

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .users import User
from .utils import now


class Chat(Base):
    __tablename__ = "chats"

    id: Mapped[uuid.UUID] = mapped_column(default=uuid.uuid4, primary_key=True)

    is_personal: Mapped[bool]

    created_at: Mapped[datetime] = mapped_column(default=now)

    messages: Mapped[list["Message"]] = relationship(
        back_populates="chat",
        order_by="desc(Message.created_at)",
    )
    last_message: Mapped["Message"] = relationship(
        back_populates="chat",
        order_by="desc(Message.created_at)",
        lazy=False,
        overlaps="messages",
    )
    members: Mapped[list["ChatMember"]] = relationship(back_populates="chat", lazy=False)


class Message(Base):
    __tablename__ = "messages"

    id: Mapped[uuid.UUID] = mapped_column(default=uuid.uuid4, primary_key=True)

    chat_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("chats.id"))
    member_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("chat_members.id"))
    text: Mapped[str] = mapped_column(String(2048))

    created_at: Mapped[datetime] = mapped_column(default=now)
    updated_at: Mapped[datetime] = mapped_column(default=now, onupdate=now)

    chat: Mapped[Chat] = relationship(back_populates="messages")
    member: Mapped["ChatMember"] = relationship(back_populates="messages")


class ChatMember(Base):
    __tablename__ = "chat_members"

    id: Mapped[uuid.UUID] = mapped_column(default=uuid.uuid4, primary_key=True)

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    chat_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("chats.id"))

    leave_at: Mapped[datetime | None]
    join_at: Mapped[datetime] = mapped_column(default=now)

    user: Mapped[User] = relationship()
    chat: Mapped[Chat] = relationship(back_populates="members")

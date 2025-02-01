from uuid import UUID

from sqlmodel import Field, Index, UniqueConstraint

from src.dal.mixins import (
    ChatIdMixin,
    CreatedAtMixin,
    IdMixin,
    LastSeenMixin,
    MessageIdMixin,
    OwnerIdMixin,
    SoftDeleteMixin,
    UserIdMixin,
)


class User(IdMixin, CreatedAtMixin, SoftDeleteMixin, table=True):  # type: ignore[call-arg]
    __tablename__ = "user"
    username: str = Field(unique=True, nullable=False, description="User login")
    is_active: bool = Field(default=True, description="Is user active")


class UserChat(IdMixin, UserIdMixin, ChatIdMixin, CreatedAtMixin, LastSeenMixin, table=True):  # type: ignore[call-arg]
    __tablename__ = "user_chat"
    __table_args__ = (
        UniqueConstraint("user_id", "chat_id", name="user_chat_unique"),
        Index("ix_user_chat_user_id", "user_id"),
        Index("ix_user_chat_chat_id", "chat_id"),
    )


class UserMessage(IdMixin, UserIdMixin, MessageIdMixin, CreatedAtMixin, table=True):  # type: ignore[call-arg]
    __tablename__ = "user_message"
    __table_args__ = (
        UniqueConstraint("user_id", "message_id", name="user_message_unique"),
        Index("ix_user_message_user_id", "user_id"),
        Index("ix_user_message_message_id", "message_id"),
    )


class ChatMessage(IdMixin, ChatIdMixin, MessageIdMixin, CreatedAtMixin, table=True):  # type: ignore[call-arg]
    __tablename__ = "chat_message"
    __table_args__ = (
        UniqueConstraint("chat_id", "message_id", name="chat_message_unique"),
        Index("ix_chat_message_chat_id", "chat_id"),
        Index("ix_chat_message_message_id", "message_id"),
    )


class Message(IdMixin, CreatedAtMixin, SoftDeleteMixin, table=True):  # type: ignore[call-arg]
    __tablename__ = "message"
    content: str = Field(allow_mutation=True, nullable=False, description="Message content")


class Chat(IdMixin, CreatedAtMixin, OwnerIdMixin, SoftDeleteMixin, table=True):  # type: ignore[call-arg]
    __tablename__ = "chat"
    name: str = Field(unique=True, nullable=False, description="Chat name")
    is_private: bool = Field(default=False, description="Is chat private")


class File(IdMixin, OwnerIdMixin, CreatedAtMixin, SoftDeleteMixin, table=True):  # type: ignore[call-arg]
    __tablename__ = "file"
    filename: str = Field(description="File name")
    content: bytes = Field(description="File content")


class ChatFile(IdMixin, ChatIdMixin, CreatedAtMixin, table=True):  # type: ignore[call-arg]
    __tablename__ = "chat_file"
    __table_args__ = (
        UniqueConstraint("chat_id", "file_id", name="chat_file_unique"),
        Index("ix_chat_file_chat_id", "chat_id"),
        Index("ix_chat_file_file_id", "file_id"),
    )
    file_id: UUID = Field(foreign_key="file.id", description="File identifier", ondelete="CASCADE")


class ChatInvite(IdMixin, CreatedAtMixin, table=True):  # type: ignore[call-arg]
    __tablename__ = "chat_invite"
    __table_args__ = (Index("ix_chat_invite_token", "token"),)
    chat_id: UUID = Field(foreign_key="chat.id", nullable=False)
    inviter_id: UUID = Field(foreign_key="user.id", nullable=False)
    token: str = Field(unique=True, nullable=False)
    is_accepted: bool = Field(default=False)

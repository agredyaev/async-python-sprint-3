from collections.abc import Sequence
from uuid import UUID

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.dal.models import Chat, ChatMessage, Message, User, UserChat
from src.dal.repositories.base import BaseRepository


class UserChatRepository(BaseRepository[UserChat]):
    model: type[UserChat] = UserChat

    def __init__(self, session: AsyncSession):
        super().__init__(session=session)

    async def create(self, user_id: UUID, chat_id: UUID) -> UserChat:
        user = await self.session.get(User, user_id)
        if not user:
            raise ValueError(f"User with id {user_id} not found")

        chat = await self.session.get(Chat, chat_id)
        if not chat:
            raise ValueError(f"Chat with id {chat_id} not found")

        user_chat = self.model(user_id=user_id, chat_id=chat_id)
        await self.upsert(user_chat)
        return user_chat

    async def add_members(self, user_ids: list[UUID], chat_id: UUID) -> None:
        members = [self.model(user_id=user_id, chat_id=chat_id) for user_id in user_ids]
        await self.bulk_create(members)

    async def get_user_chats(self, user_id: UUID) -> Sequence[Chat]:
        """Get all chats where user is a member."""
        statement = select(Chat).join(self.model, self.model.chat_id == Chat.id).where(self.model.user_id == user_id)
        return await self.get_all(statement)

    async def get_unread_messages_count(self, user_id: UUID, chat_id: UUID) -> int:
        """Get count of unread messages for user in specific chat."""
        statement = (
            select(Message)
            .join(ChatMessage, ChatMessage.message_id == Message.id)
            .join(self.model, self.model.chat_id == ChatMessage.chat_id)
            .where(
                ChatMessage.chat_id == chat_id,
                self.model.user_id == user_id,
                ChatMessage.created_at > UserChat.last_seen,
            )
        )
        result = await self.get_all(statement)
        return len(result)

    async def get_user_chat(self, user_id: UUID, chat_id: UUID) -> UserChat:
        statement = select(self.model).where(self.model.chat_id == chat_id, self.model.user_id == user_id)
        return await self.get_by_statement(statement)

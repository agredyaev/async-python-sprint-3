from collections.abc import Sequence
from datetime import datetime
from uuid import UUID

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.core.settings import settings
from src.dal.models import Chat, ChatMessage, Message
from src.dal.repositories.base import BaseRepository


class ChatMessageRepository(BaseRepository[ChatMessage]):
    model: type[ChatMessage] = ChatMessage

    def __init__(self, session: AsyncSession):
        super().__init__(session=session)

    async def create(self, chat_id: UUID, message_id: UUID) -> ChatMessage:
        chat = await self.session.get(Chat, chat_id)
        if not chat:
            raise ValueError(f"Chat with id {chat_id} not found")

        message = await self.session.get(Message, message_id)
        if not message:
            raise ValueError(f"Message with id {message_id} not found")

        chat_message = self.model(chat_id=chat_id, message_id=message_id)
        await self.upsert(chat_message)
        return chat_message

    async def get_by_chat_id(self, chat_id: UUID) -> Sequence[ChatMessage]:
        statement = select(self.model).where(self.model.chat_id == chat_id)
        return await self.get_all(statement)

    async def get_last_messages(self, chat_id: UUID) -> Sequence[Message]:
        statement = (
            select(Message).join(self.model, self.model.message_id == Message.id).where(self.model.chat_id == chat_id)
        )
        return await self.get_all(statement, order_by=Message.created_at, limit=settings.server.message_limit)

    async def get_unread_messages(self, chat_id: UUID, last_seen: datetime) -> Sequence[Message]:
        statement = (
            select(Message)
            .join(self.model, self.model.message_id == Message.id)
            .where(self.model.chat_id == chat_id, ChatMessage.created_at > last_seen)
        )
        return await self.get_all(statement)

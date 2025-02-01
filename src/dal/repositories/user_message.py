from uuid import UUID

from sqlmodel.ext.asyncio.session import AsyncSession

from src.dal.models import Message, User, UserMessage
from src.dal.repositories.base import BaseRepository


class UserMessageRepository(BaseRepository[UserMessage]):
    model: type[UserMessage] = UserMessage

    def __init__(self, session: AsyncSession):
        super().__init__(session=session)

    async def create(self, user_id: UUID, message_id: UUID) -> UserMessage:
        user = await self.session.get(User, user_id)
        if not user:
            raise ValueError(f"User with id {user_id} not found")

        message = await self.session.get(Message, message_id)
        if not message:
            raise ValueError(f"Message with id {message_id} not found")

        user_message = self.model(user_id=user_id, message_id=message_id)
        await self.upsert(user_message)
        return user_message

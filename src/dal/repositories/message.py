from sqlmodel.ext.asyncio.session import AsyncSession

from src.dal.models import Message
from src.dal.repositories.base import BaseRepository


class MessageRepository(BaseRepository[Message]):
    model: type[Message] = Message

    def __init__(self, session: AsyncSession):
        super().__init__(session=session)

    async def create(self, content: str) -> Message:
        message = self.model(content=content)
        await self.upsert(message)
        return message

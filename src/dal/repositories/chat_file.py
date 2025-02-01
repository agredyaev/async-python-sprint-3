from uuid import UUID

from sqlmodel.ext.asyncio.session import AsyncSession

from src.dal.models import Chat, ChatFile, File
from src.dal.repositories.base import BaseRepository


class ChatFileRepository(BaseRepository[ChatFile]):
    model: type[ChatFile] = ChatFile

    def __init__(self, session: AsyncSession):
        super().__init__(session=session)

    async def create(self, chat_id: UUID, file_id: UUID) -> ChatFile:
        chat = await self.session.get(Chat, chat_id)
        if not chat:
            raise ValueError(f"Chat with id {chat_id} not found")

        file = await self.session.get(File, file_id)
        if not file:
            raise ValueError(f"File with id {file_id} not found")

        chat_file = self.model(chat_id=chat_id, file_id=file_id)
        await self.upsert(chat_file)
        return chat_file

from sqlmodel.ext.asyncio.session import AsyncSession

from src.dal.models import File, User
from src.dal.repositories.base import BaseRepository


class FileRepository(BaseRepository[File]):
    model: type[File] = File

    def __init__(self, session: AsyncSession):
        super().__init__(session=session)

    async def create(self, dto) -> File:  # type: ignore[no-untyped-def]
        owner = await self.session.get(User, dto.user_id)
        if not owner:
            raise ValueError(f"User with id {dto.user_id} not found")

        file = self.model(filename=dto.file.name, content=dto.file.content, owner_id=dto.user_id)
        await self.upsert(file)
        return file

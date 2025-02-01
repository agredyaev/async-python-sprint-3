from sqlmodel.ext.asyncio.session import AsyncSession

from src.core.exceptions import FileUploadError
from src.dal import ChatFileRepository, FileRepository
from src.schemas.api import Body, Response, StatusCode
from src.schemas.services import UploadRequest


class FileService:
    """File service."""

    __slots__ = ("chat_file_repo", "file_repo")

    def __init__(self, session: AsyncSession):
        self.file_repo = FileRepository(session=session)
        self.chat_file_repo = ChatFileRepository(session=session)

    async def upload(self, data: UploadRequest) -> Response:
        try:
            file = await self.file_repo.create(data)
            chat_file = await self.chat_file_repo.create(chat_id=data.chat.id, file_id=file.id)
        except FileUploadError as e:
            return Response(status_code=StatusCode.BAD_REQUEST, body=Body(details=str(e)))
        else:
            return Response(
                status_code=StatusCode.OK, body=Body(details=f"file_id: {file.id}, chat_file_id: {chat_file.id}")
            )

from pydantic import ConfigDict, Field

from src.core.settings import settings
from src.schemas.mixins import StrippingMixin
from src.schemas.services.chat import ChatConnect


class FileInput(StrippingMixin):
    name: str = Field(min_length=4, max_length=15, description="User login")
    content: bytes = Field(min_length=1, max_length=settings.server.max_file_size_bytes, description="File content")


class UploadRequest(ChatConnect):
    file: FileInput

    model_config = ConfigDict(frozen=True)

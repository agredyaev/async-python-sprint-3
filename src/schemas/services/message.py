from pydantic import BaseModel

from src.schemas.services.chat import ChatConnect


class MessageCreate(BaseModel):
    content: str
    connect: ChatConnect

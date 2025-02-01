from uuid import UUID

from pydantic import Field

from src.schemas.mixins import StrippingMixin


class UserInput(StrippingMixin):
    username: str = Field(description="User login")


class UserId(StrippingMixin):
    id: UUID

from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from src.schemas.api.enums import StatusCode
from src.schemas.mixins import BaseMixin


class Header(BaseModel):
    name: str
    value: str


class Body(BaseModel):
    details: Any


class Response(BaseMixin):
    status_code: StatusCode
    headers: list[Header] = Field(default_factory=lambda: [Header(name="Content-Type", value="application/json")])
    body: Body

    model_config = ConfigDict(frozen=True)

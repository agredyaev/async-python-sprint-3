from typing import Any

from datetime import datetime

from pydantic import BaseModel, ConfigDict, field_validator
from pydantic_core.core_schema import ValidationInfo


class BaseMixin(BaseModel):
    model_config = ConfigDict(
        json_encoders={datetime: lambda dt: dt.isoformat()}, use_enum_values=True, str_strip_whitespace=True
    )


class StrippingMixin(BaseMixin):
    @field_validator("*", mode="before")
    @classmethod
    def strip_and_check_not_empty(cls, value: Any, info: ValidationInfo) -> Any:
        if isinstance(value, str) and not value:
            raise ValueError(f"[{cls.__name__}] field {info.field_name} cannot be empty.")
        return value

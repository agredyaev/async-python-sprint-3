from typing import Any

from urllib.parse import parse_qs, urlparse

from pydantic import BaseModel, ConfigDict, Field, model_validator

from src.schemas.api.enums import Method, Path
from src.schemas.mixins import BaseMixin


class Endpoint(BaseMixin):
    path: Path = Field(description="Path of the endpoint")
    method: Method = Field(description="Method of the endpoint")

    model_config = ConfigDict(frozen=True)


class Request(BaseModel):
    raw_request_line: str = Field(description="Raw request line")
    endpoint: Endpoint = Field(description="Endpoint of the request")
    data: dict[str, Any] = Field(description="Data of the request")
    query_params: dict[str, Any] = Field(description="Query parameters of the request")

    @model_validator(mode="before")
    @classmethod
    def parse_request(cls, data: dict[str, Any]) -> dict[str, Any]:
        """Parse the raw request line and extract the endpoint, data, and query parameters."""

        raw_request_line = data.get("raw_request_line")
        if not raw_request_line:
            raise ValueError("Missing raw request line")

        parts = raw_request_line.strip().split(" ")
        if len(parts) < 2:
            raise ValueError(f"Invalid request: {' '.join(parts)}")

        method_part, raw_path, *_ = parts
        parsed = urlparse(raw_path)

        query_params = parse_qs(parsed.query)
        query_params = {k: val[0] for k, val in query_params.items()}  # type: ignore[misc]

        try:
            endpoint = Endpoint(path=Path(parsed.path), method=Method(method_part))
        except ValueError as error:
            raise ValueError(f"Invalid request: {error!s}") from error

        return {
            "raw_request_line": raw_request_line,
            "endpoint": endpoint,
            "data": data.get("data", {}),
            "query_params": query_params,
        }

from typing import Any

import asyncio
import json

from src.core.logger import get_logger
from src.core.settings import settings
from src.schemas.api import Response

logger = get_logger("client")


class ChatClient:
    """Client for connecting to a chat server."""

    def __init__(self, host: str = "127.0.0.1", port: int = 8080, buffer_size: int = 1024) -> None:
        self.host = host
        self.port = port
        self.buffer_size = buffer_size
        self.reader: asyncio.StreamReader | None = None
        self.writer: asyncio.StreamWriter | None = None

    async def connect(self) -> None:
        logger.info("Connecting to server on %s:%s", self.host, self.port)
        self.reader, self.writer = await asyncio.open_connection(self.host, self.port)
        logger.info("Connected to server on %s:%s", self.host, self.port)

    async def disconnect(self) -> None:
        if self.writer:
            self.writer.close()
            await self.writer.wait_closed()

    async def send_request(self, method: str, path: str, data: dict[str, Any]) -> Response:
        if not self.writer or not self.reader:
            logger.exception("Not connected to server", exc_info=True)
            raise ConnectionError("Not connected to server")

        request_dict = {"raw_request_line": f"{method} {path} HTTP/1.1", "data": data}
        full_request = json.dumps(request_dict)
        logger.info("Sending request: %s", full_request)

        self.writer.write(full_request.encode())
        await self.writer.drain()

        try:
            async with asyncio.timeout(settings.server.timeout_seconds):
                response_data = await self.reader.read(self.buffer_size)
                if not response_data:
                    raise RuntimeError("No response from server")
        except TimeoutError:
            logger.warning("Request timed out after %d seconds", settings.server.timeout_seconds)
            raise RuntimeError("Request timed out") from None
        else:
            return Response.model_validate_json(response_data.decode())

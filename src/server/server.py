import asyncio

from src.core.logger import get_logger
from src.core.settings import ServerSettings
from src.schemas.api import Body, Request, Response, StatusCode
from src.server.router import Router

logger = get_logger("server")


class CustomAsyncServer:
    """Custom AsyncHTTPServer."""

    __slots__ = ("_config", "_router")

    def __init__(self, config: ServerSettings, router: Router) -> None:
        self._config = config
        self._router = router

    async def start(self) -> None:
        """Start the server."""
        logger.info("Starting server on %s:%s", self._config.host, self._config.port)
        server = await asyncio.start_server(self._handle_client, self._config.host, self._config.port)
        addr = server.sockets[0].getsockname() if server.sockets else None
        logger.info("Server started on %s", addr)
        async with server:
            await server.serve_forever()

    async def _handle_client(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        logger.info("New connection accepted")
        try:
            while not reader.at_eof():
                data = await reader.read(self._config.buffer_size_bytes)
                if not data:
                    break
                logger.info("Received data: %s", data)
                request = Request.model_validate_json(data)
                response = await self._router.resolve(request)

                writer.write(response.model_dump_json().encode())
                await writer.drain()

        except Exception as e:
            logger.exception("Unhandled exception occurred", exc_info=e)
            error_response = Response(status_code=StatusCode.INTERNAL_SERVER_ERROR, body=Body(details=f"{e!s}"))
            writer.write(error_response.model_dump_json().encode())
            await writer.drain()
        finally:
            writer.close()
            await writer.wait_closed()
            logger.info(msg="Connection closed")

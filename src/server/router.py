from collections.abc import Awaitable, Callable

from pydantic import ValidationError

from src.core.exceptions import InternalError, NotFoundError
from src.core.logger import get_logger
from src.schemas.api import Body, Endpoint, Request, Response, StatusCode

logger = get_logger("router")


class Router:
    """Router for handling incoming requests."""

    __slots__ = ("routes",)

    def __init__(self) -> None:
        self.routes: dict[Endpoint, Callable[..., Awaitable[Response]]] = {}

    def add_route(self, path: Endpoint, handler: Callable[..., Awaitable[Response]]) -> None:
        """Registers a new route with the router."""
        self.routes[path] = handler
        logger.info("Route %s added", path)

    async def resolve(self, request: Request) -> Response:
        """Handles an incoming request and returns the response."""
        handler = self.routes.get(request.endpoint)
        if not handler:
            logger.info("Route %s %s not found", request.endpoint.path, request.endpoint.method)
            return Response(
                status_code=StatusCode.NOT_FOUND,
                body=Body(details=f"Route {request.endpoint.path} {request.endpoint.method} Not found"),
            )
        try:
            return await handler(request.data)
        except ValidationError as e:
            logger.info("Validation error: %s", e.errors())
            return Response(status_code=StatusCode.BAD_REQUEST, body=Body(details=e.errors()))
        except NotFoundError as e:
            logger.exception(msg="Not found error", exc_info=e)
            return Response(status_code=StatusCode.NOT_FOUND, body=Body(details=str(e)))
        except InternalError as e:
            logger.exception(msg="Internal error", exc_info=e)
            return Response(status_code=StatusCode.INTERNAL_SERVER_ERROR, body=Body(details=str(e)))

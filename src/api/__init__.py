from typing import Any

from collections.abc import Awaitable, Callable

from schemas.api import Response
from src.dal.db import get_session
from src.schemas.api import Endpoint, Method, Path
from src.server.router import Router
from src.services import ChatService, FileService, InviteService, MessageService


def with_session(service_cls: type, method_name: str) -> Callable[[dict[str, Any]], Awaitable[Response]]:
    async def route_handler(data: dict[str, Any]) -> Response:
        async with get_session() as session:
            service = service_cls(session)
            method = getattr(service, method_name)
            return await method(data)

    return route_handler


async def build_routes_factory() -> Router:
    router = Router()

    routes_config = [
        (Endpoint(path=Path.CREATE_CHAT, method=Method.POST), ChatService, "create_chat"),
        (Endpoint(path=Path.CONNECT, method=Method.POST), ChatService, "connect"),
        (Endpoint(path=Path.UPLOAD_FILE, method=Method.POST), FileService, "upload"),
        (Endpoint(path=Path.CHAT_GENERATE_INVITE, method=Method.POST), InviteService, "generate_invite_link"),
        (Endpoint(path=Path.CHAT_ACCEPT_INVITE, method=Method.POST), InviteService, "accept_invite"),
        (Endpoint(path=Path.SEND, method=Method.POST), MessageService, "send_message"),
        (Endpoint(path=Path.STATUS, method=Method.GET), ChatService, "get_status"),
        (Endpoint(path=Path.CREATE_USER, method=Method.POST), ChatService, "create_user"),
        (Endpoint(path=Path.GET_USER_ID, method=Method.GET), ChatService, "get_user_id"),
    ]

    for endpoint, service_cls, method_name in routes_config:
        router.add_route(endpoint, with_session(service_cls, method_name))

    return router

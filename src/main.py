import asyncio

from src.api import build_routes_factory
from src.core.logger import get_logger
from src.core.settings import settings
from src.helpers import requires_python_version
from src.server import CustomAsyncServer

logger = get_logger("main")


@requires_python_version()
async def main() -> None:
    router_factory = await build_routes_factory()

    server = CustomAsyncServer(settings.server, router_factory)
    await server.start()


if __name__ == "__main__":
    asyncio.run(main())

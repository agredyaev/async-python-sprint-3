import asyncio

import pytest

from pytest_mock import MockerFixture

from src.core.exceptions import BaseError
from src.core.settings import ServerSettings
from src.schemas.api import Body, Request, Response, StatusCode
from src.server.router import Router
from src.server.server import CustomAsyncServer
from tests.factories import BodyFactory, ResponseFactory, ServerSettingsFactory


@pytest.fixture
def mock_request():
    return Request(raw_request_line="GET /create_chat?room=general HTTP/1.1")


@pytest.fixture
def server_settings() -> ServerSettings:
    return ServerSettingsFactory.build(host="127.0.0.1", port=8000, buffer_size=1024)


@pytest.fixture
def mock_router(mocker: MockerFixture) -> Router:
    router = mocker.create_autospec(Router, instance=True)
    router.resolve = mocker.AsyncMock()
    return router


@pytest.fixture
def server(server_settings: ServerSettings, mock_router: Router) -> CustomAsyncServer:
    return CustomAsyncServer(config=server_settings, router=mock_router)


@pytest.mark.asyncio
async def test_handle_client_success(
    server: CustomAsyncServer, mock_router: Router, mocker: MockerFixture, mock_request: Request
):
    mock_reader = mocker.AsyncMock(spec=asyncio.StreamReader)
    mock_writer = mocker.AsyncMock(spec=asyncio.StreamWriter)

    response = ResponseFactory.build(
        status_code=StatusCode.OK, body=BodyFactory.build(details="Success", message="Test")
    )

    mock_reader.at_eof.return_value = False
    mock_reader.read.side_effect = [mock_request.model_dump_json().encode("utf-8"), b""]
    mock_router.resolve.return_value = response

    await server._handle_client(mock_reader, mock_writer)

    mock_router.resolve.assert_called_once_with(mock_request)
    mock_writer.write.assert_called_once_with(response.model_dump_json().encode())
    mock_writer.drain.assert_called_once()
    mock_writer.close.assert_called_once()
    mock_writer.wait_closed.assert_called_once()


@pytest.mark.asyncio
async def test_handle_client_internal_error(
    server: CustomAsyncServer, mock_router: Router, mocker: MockerFixture, mock_request: Request
):
    mock_reader = mocker.AsyncMock(spec=asyncio.StreamReader)
    mock_writer = mocker.AsyncMock(spec=asyncio.StreamWriter)

    mock_reader.at_eof.return_value = False
    mock_reader.read.side_effect = [mock_request.model_dump_json().encode("utf-8"), b""]
    mock_router.resolve.side_effect = Exception("Test error")

    await server._handle_client(mock_reader, mock_writer)

    expected_response = Response(status_code=StatusCode.INTERNAL_SERVER_ERROR, body=Body(details="Test error"))

    mock_writer.write.assert_called_once_with(expected_response.model_dump_json().encode())
    mock_writer.drain.assert_called()
    mock_writer.close.assert_called_once()
    mock_writer.wait_closed.assert_called_once()


@pytest.mark.asyncio
async def test_start_server(server: CustomAsyncServer, mocker: MockerFixture):
    mock_start_server = mocker.AsyncMock()
    mock_server = mocker.AsyncMock()
    mock_start_server.return_value = mock_server
    mocker.patch("asyncio.start_server", mock_start_server)

    await server.start()

    mock_start_server.assert_called_once_with(server._handle_client, server._config.host, server._config.port)
    mock_server.serve_forever.assert_called_once()

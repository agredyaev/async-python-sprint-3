import pytest

from pydantic import ValidationError
from pytest_mock import MockerFixture

from src.core.exceptions import InternalError
from src.schemas.api import Endpoint, Method, Path, Request, Response, StatusCode
from src.server.router import Router
from tests.factories import BodyFactory


@pytest.fixture
def router():
    return Router()


@pytest.fixture
def mock_request():
    return Request(raw_request_line="GET /create_chat?room=general HTTP/1.1")


@pytest.fixture
def mock_request_exists():
    return Request(raw_request_line="POST /create_chat?room=general HTTP/1.1")


@pytest.fixture
def mock_endpoint_exists():
    return Endpoint(path=Path.CREATE_CHAT, method=Method.POST)


@pytest.mark.asyncio
async def test_add_route(router: Router, mock_endpoint_exists: Endpoint):
    async def handler(data):  # noqa: ARG001
        return BodyFactory.build()

    router.add_route(mock_endpoint_exists, handler)
    assert mock_endpoint_exists in router.routes


@pytest.mark.asyncio
async def test_resolve_existing_route(router: Router, mocker: MockerFixture, mock_request_exists: Request):
    endpoint = mock_request_exists.endpoint
    mock_response_body = BodyFactory.build()
    mock_handler = mocker.AsyncMock(return_value=Response(status_code=StatusCode.OK, body=mock_response_body))

    router.add_route(endpoint, mock_handler)
    assert endpoint in router.routes, "Route was not properly registered"

    response = await router.resolve(mock_request_exists)

    assert response is not None, "Response is None"
    assert response.status_code == StatusCode.OK.value, "Status code is not OK"
    assert response.body == mock_response_body, "Response body is not expected"
    mock_handler.assert_called_once_with(mock_request_exists.data), "Handler was not called"


@pytest.mark.asyncio
async def test_resolve_nonexistent_route(router: Router, mock_request: Request):
    request = mock_request
    response = await router.resolve(request)

    assert response.status_code == StatusCode.NOT_FOUND.value
    assert "Not found" in response.body.details


@pytest.mark.asyncio
async def test_resolve_validation_error(router: Router, mocker: MockerFixture, mock_request: Request):
    endpoint = mock_request.endpoint
    mock_handler = mocker.AsyncMock(
        side_effect=ValidationError.from_exception_data(
            title="",
            line_errors=[
                {
                    "type": "value_error",
                    "loc": ("field",),
                    "msg": "Invalid value",
                    "input": None,
                    "ctx": {"error": ValueError("Invalid value")},
                }
            ],
        )
    )
    router.add_route(endpoint, mock_handler)

    assert endpoint in router.routes, "Route was not added"

    request = mock_request
    response = await router.resolve(request)

    assert response.status_code == StatusCode.BAD_REQUEST.value, "Status code is not BAD_REQUEST"
    assert "Invalid value" in str(response.body.details), "Error message is not expected"


@pytest.mark.asyncio
async def test_resolve_internal_error(router: Router, mocker: MockerFixture, mock_request: Request):
    endpoint = mock_request.endpoint
    mock_handler = mocker.AsyncMock(side_effect=InternalError("Test internal error"))
    router.add_route(endpoint, mock_handler)

    request = mock_request
    response = await router.resolve(request)

    assert response.status_code == StatusCode.INTERNAL_SERVER_ERROR.value, "Status code is not INTERNAL_SERVER_ERROR"
    assert "Test internal error" in response.body.details, "Error message is not expected"

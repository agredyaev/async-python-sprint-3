import pytest
import pytest_asyncio

from sqlmodel.ext.asyncio.session import AsyncSession

from src.core.exceptions import BaseError
from src.schemas.api import Body, StatusCode
from src.services.message import MessageService
from tests.factories import MessageCreateFactory, MessageFactory


@pytest_asyncio.fixture
async def message_service(mocker):
    session = mocker.Mock(spec=AsyncSession)
    return MessageService(session=session)


@pytest.mark.asyncio
async def test_send_message_success(message_service, mocker):
    message_data = MessageCreateFactory.build()
    mock_message = MessageFactory.build()

    message_service.user_chat_repo.get_user_chat = mocker.AsyncMock(return_value=True)
    message_service.message_repo.create = mocker.AsyncMock(return_value=mock_message)
    message_service.chat_message_repo.create = mocker.AsyncMock()
    message_service.user_message_repo.create = mocker.AsyncMock()

    response = await message_service.send_message(message_data)

    assert response.status_code == StatusCode.OK
    assert isinstance(response.body, Body)
    assert f"message_id {mock_message.id}" in response.body.details
    message_service.message_repo.create.assert_awaited_once_with(content=message_data.content)


@pytest.mark.asyncio
async def test_send_message_user_not_in_chat(message_service, mocker):
    message_data = MessageCreateFactory.build()
    message_service.user_chat_repo.get_user_chat = mocker.AsyncMock(return_value=False)

    response = await message_service.send_message(message_data)

    assert response.status_code == StatusCode.BAD_REQUEST
    assert isinstance(response.body, Body)
    assert "User is not a member of the chat" in response.body.details


@pytest.mark.asyncio
async def test_send_message_database_error(message_service, mocker):
    message_data = MessageCreateFactory.build()
    message_service.user_chat_repo.get_user_chat = mocker.AsyncMock(return_value=True)
    message_service.message_repo.create = mocker.AsyncMock(side_effect=BaseError("Database error"))

    with pytest.raises(BaseError) as exc_info:
        await message_service.send_message(message_data)
    assert str(exc_info.value) == "Database error"

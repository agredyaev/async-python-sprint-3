from uuid import uuid4

import pytest

from src.core.exceptions import BaseError
from src.schemas.api import StatusCode
from src.schemas.services.chat import ChatResponse
from src.services import ChatService
from tests.factories import ChatConnectFactory, ChatCreateFactory, ChatFactory, MessageFactory


@pytest.mark.asyncio
async def test_create_chat_success(mocker):
    session_mock = mocker.AsyncMock()
    chat_service = ChatService(session=session_mock)

    chat_data = ChatCreateFactory.build()
    mock_chat = mocker.Mock(id=uuid4(), name="Test Chat")

    chat_service.chat_repo.create = mocker.AsyncMock(return_value=mock_chat)
    chat_service.user_chat_repo.add_members = mocker.AsyncMock()

    response = await chat_service.create_chat(chat_data)

    assert response.status_code == StatusCode.CREATED
    assert "chat_id" in response.body.details
    assert "name" in response.body.details
    chat_service.chat_repo.create.assert_awaited_once_with(data=chat_data)
    chat_service.user_chat_repo.add_members.assert_awaited_once_with(
        user_ids=[member.id for member in chat_data.members], chat_id=mock_chat.id
    )


@pytest.mark.asyncio
async def test_connect_success(mocker):
    session_mock = mocker.AsyncMock()
    chat_service = ChatService(session=session_mock)

    connect_data = ChatConnectFactory.build()
    mock_chat = mocker.Mock(id=connect_data.chat.id)
    mock_user_chat = mocker.Mock(last_seen=None)

    last_messages = [MessageFactory.build() for _ in range(3)]
    unread_messages = [MessageFactory.build() for _ in range(2)]

    chat_service.chat_repo.get = mocker.AsyncMock(return_value=mock_chat)
    chat_service.user_chat_repo.get_user_chat = mocker.AsyncMock(return_value=mock_user_chat)
    chat_service.chat_message_repo.get_last_messages = mocker.AsyncMock(return_value=last_messages)
    chat_service.chat_message_repo.get_unread_messages = mocker.AsyncMock(return_value=unread_messages)

    response = await chat_service.connect(connect_data)

    assert response.status_code == StatusCode.OK
    assert isinstance(response.body.details, ChatResponse)

    chat_service.chat_repo.get.assert_awaited_once_with(connect_data.chat.id)
    chat_service.user_chat_repo.get_user_chat.assert_awaited_once_with(connect_data.user.id, connect_data.chat.id)


@pytest.mark.asyncio
async def test_connect_chat_not_found(mocker):
    session_mock = mocker.AsyncMock()
    chat_service = ChatService(session=session_mock)

    connect_data = ChatConnectFactory.build()

    chat_service.chat_repo.get = mocker.AsyncMock(return_value=None)

    with pytest.raises(BaseError) as exc_info:
        await chat_service.connect(connect_data)

    assert "Chat with id" in str(exc_info.value)


@pytest.mark.asyncio
async def test_get_status_success(mocker):
    session_mock = mocker.AsyncMock()
    chat_service = ChatService(session=session_mock)

    user_id = uuid4()

    user_chats = [ChatFactory.build() for _ in range(2)]

    chat_service.user_chat_repo.get_user_chats = mocker.AsyncMock(return_value=user_chats)
    chat_service.user_chat_repo.get_unread_messages_count = mocker.AsyncMock(return_value=3)

    response = await chat_service.get_status({"id": user_id})

    assert response.status_code == StatusCode.OK
    assert len(response.body.details) == len(user_chats)

    for status in response.body.details:
        assert status.unread_messages_count == 3
        assert status.chat.name == "Test Chat"

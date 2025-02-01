from typing import Any

import asyncio
import os
import sys

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from pathlib import Path
from uuid import UUID, uuid4

import pytest
import pytest_asyncio

from faker.proxy import Faker

from src.client.client import ChatClient
from src.core.exceptions import BaseError
from src.core.settings import settings

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 9090


@asynccontextmanager
async def start_server_context() -> AsyncGenerator[None, Any]:
    process = await asyncio.create_subprocess_exec(
        sys.executable, "src/main.py", stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE, cwd="."
    )
    try:
        while True:
            line = await process.stdout.readline()
            if "Server started on" in line.decode():
                break
            if process.returncode is not None:
                error = await process.stderr.read()
                raise RuntimeError(f"Server failed to start: {error.decode()}")
            await asyncio.sleep(0.1)

        yield process
    finally:
        process.terminate()
        await process.wait()


@pytest_asyncio.fixture(scope="module")
async def server() -> AsyncGenerator[None, None]:
    async with start_server_context() as proc:
        yield proc


@pytest_asyncio.fixture
async def client() -> AsyncGenerator[ChatClient, None]:
    chat_client = ChatClient(host=SERVER_HOST, port=SERVER_PORT)
    await chat_client.connect()
    try:
        yield chat_client
    finally:
        await chat_client.disconnect()


@pytest.fixture(scope="module")
def test_ids():
    user_id = str(uuid4())
    return {
        "user": {"id": user_id, "username": Faker().user_name()},
        "chat": {"name": Faker().user_name(), "is_private": False},
    }


async def check_port(host: str, port: int) -> bool:
    try:
        reader, writer = await asyncio.open_connection(host, port)
        writer.close()
        await writer.wait_closed()
    except BaseError:
        return False
    else:
        return True


@pytest.mark.asyncio
async def test_server_is_running(server):
    assert server is not None, "Server process is not running"
    is_open = await check_port(SERVER_HOST, SERVER_PORT)
    assert is_open, "Server is not accepting connections"


@pytest.mark.asyncio
async def test_create_user(client: ChatClient, test_ids: dict[str, Any]):
    username = test_ids["user"]["username"]
    response = await client.send_request(method="POST", path="/create_user", data={"username": username})

    assert response is not None, "Response is None"
    assert response.status_code == 201
    assert "username" in response.body.details


@pytest.mark.asyncio
async def test_connect_to_chat(client: ChatClient, test_ids: dict[str, UUID], default_settings):
    username = test_ids["user"]["username"]
    user = await client.send_request(method="GET", path="/get_user_id", data={"username": username})

    assert user is not None, "User is None"
    assert user.status_code == 200

    chat = test_ids["chat"]
    chat_new = await client.send_request(
        method="POST", path="/create_chat", data={"chat": chat, "owner": {"id": user.body.details}}
    )

    assert chat_new is not None, "Chat is None"
    assert chat_new.status_code == 201
    assert chat["name"] in chat_new.body.details

    response = await client.send_request(
        method="POST",
        path="/connect",
        data={"user": {"id": str(user.body.details)}, "chat": {"id": str(default_settings.server.default_chat_uuid)}},
    )

    assert response.status_code == 200
    assert "last_messages" in response.body.details

    chat_id = chat_new.body.details.split(",")[0].split(":")[-1].strip()

    response = await client.send_request(
        method="POST",
        path="/send",
        data={"content": "Hello, world!", "connect": {"user": {"id": user.body.details}, "chat": {"id": chat_id}}},
    )

    assert response is not None, "Response is None"
    assert response.status_code == 200, "Response status code is not 200"
    assert "message_id" in response.body.details

    response = await client.send_request(method="GET", path="/status", data={"id": user.body.details})

    assert response.status_code == 200
    assert isinstance(response.body.details, list)

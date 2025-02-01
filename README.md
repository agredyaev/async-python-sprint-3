# Chat Application

![Python](https://img.shields.io/badge/python-3.13-blue)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Actions status](https://github.com/agredyaev/async-python-sprint-3/actions/workflows/app-testing.yml/badge.svg)](https://github.com/agredyaev/async-python-sprint-2/actions)
![Pydantic](https://img.shields.io/badge/Pydantic-red?logo=pydantic&logoColor=white)
![SQLModel](https://img.shields.io/badge/SQLModel-blue?logo=sqlmodel&logoColor=white)
[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](https://mit-license.org/)

## Overview

This project is a lightweight, asynchronous **chat application** built in Python.
The application provides the following features:
- **CustomAsyncHTTPServer**: A simple asynchronous HTTP server.
- **CustomHTTPClient**: A simple asynchronous HTTP client.
- **Chat Rooms**: Users can create and join chat rooms, both private and public.
- **File Uploads**: Upload and share files within chat rooms.
- **Invite System**: Generate unique invite links to private conversations or rooms.
- **Message History**: Retrieve message histories and keep track of unread messages.
- **Real-Time Updates**: Asynchronous server-client communication for immediate message delivery.
- **Extensible Framework**: Modular structure for adding new features and enhancements.

---

## Features

- **User Management**: Register and manage users with unique usernames.
- **Chat Creation**: Create private or public chat rooms.
- **File Sharing**: Upload files and associate them with chats.
- **Invite Links**: Secure invite tokens for accessing private chats.
- **Status Monitoring**: Retrieve chat activity and unread message counts.

---

## Documentation

The full documentation is provided in the following sections:

- [API Documentation](docs/api.md): Full details of the API endpoints, request/response schemas, and examples.
- [Layered Architecture](docs/layers.md): Breakdown of the application design into logical layers (Presentation, Business Logic, Data Access, and Infrastructure).

---
## Deploy
```bash
# clone the repository
git clone https://github.com/agredyaev/async-python-sprint-3.git
cd async-python-sprint-3
# setup the environment
make setup
# activate the virtual environment
. ./.venv/bin/activate

# run the tests
make migrate-test
```

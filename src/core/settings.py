from pathlib import Path
from uuid import UUID

from dotenv import find_dotenv, load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv(find_dotenv())


class DefaultSettings(BaseSettings):
    """Class to store default project settings."""

    root_path: Path = Path().cwd().parent.parent.resolve()

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


class PythonVersionSettings(DefaultSettings):
    """Class to store Python version settings."""

    min_major: int = Field(default=3, description="Minimum major version")
    min_minor: int = Field(default=9, description="Minimum minor version")

    model_config = SettingsConfigDict(env_prefix="PYTHON_")


class DatabaseSettings(DefaultSettings):
    """Class to store database settings."""

    url: str = Field(default=..., description="Database URL")

    model_config = SettingsConfigDict(env_prefix="DATABASE_")


class ServerSettings(DefaultSettings):
    host: str = Field(default=..., description="Server host")
    port: int = Field(default=..., ge=1, le=65535, description="Server port")
    buffer_size_bytes: int = Field(default=..., ge=512, le=65536, description="Buffer size")
    debug: bool = Field(default=..., description="Debug mode")
    max_file_size_bytes: int = Field(default=..., description="Max file size")
    message_limit: int = Field(default=..., description="Message limit")
    message_history_limit: int = Field(default=..., description="Message history limit")
    message_cooldown_seconds: int = Field(default=..., description="Message cooldown")
    token_size: int = Field(default=128, description="Token size")
    default_chat_uuid: UUID = Field(default_factory=lambda: UUID(int=0), description="Default chat uuid")
    default_chat_name: str = Field(default="General", description="Default chat name")
    default_user_uuid: UUID = Field(default_factory=lambda: UUID(int=0), description="Default user uuid")
    default_user_name: str = Field(default="Admin", description="Default user name")
    timeout_seconds: int = Field(default=30, description="Client timeout")

    model_config = SettingsConfigDict(env_prefix="SERVER_")


class Settings(BaseSettings):
    py_ver: PythonVersionSettings = PythonVersionSettings()
    db: DatabaseSettings = DatabaseSettings()
    server: ServerSettings = ServerSettings()


settings = Settings()

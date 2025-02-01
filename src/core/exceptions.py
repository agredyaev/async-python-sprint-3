class BaseError(Exception):
    __slots__ = ("message",)
    """Base exception class."""


class InternalError(BaseError):
    """Exception for internal errors."""


class StrategyError(BaseError):
    """Exception for strategy errors."""


class UnsupportedPythonVersionError(BaseError):
    """Exception for unsupported python version."""


class FileUploadError(BaseError):
    """Exception for file upload errors."""


class NotFoundError(BaseError):
    """Exception for not found errors."""

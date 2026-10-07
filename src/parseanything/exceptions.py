"""Custom exceptions and error codes for ParseAnything engine."""

from enum import Enum


class ErrorCode(str, Enum):
    FILE_NOT_FOUND = "FILE_NOT_FOUND"
    UNSUPPORTED_FORMAT = "UNSUPPORTED_FORMAT"
    PARSING_ERROR = "PARSING_ERROR"


class ParseError(Exception):
    """Custom exception raised when document parsing or format detection fails."""
    def __init__(self, message: str, code: ErrorCode = ErrorCode.PARSING_ERROR):
        super().__init__(message)
        self.message = message
        self.code = code

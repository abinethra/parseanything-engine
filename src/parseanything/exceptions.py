"""Custom exceptions and standard error codes for ParseAnything."""

class ErrorCode:
    """Standardized error codes required by DQCL specification."""
    FILE_NOT_FOUND = "FILE_NOT_FOUND"
    UNSUPPORTED_FORMAT = "UNSUPPORTED_FORMAT"
    CORRUPT_FILE = "CORRUPT_FILE"
    FILE_TOO_LARGE = "FILE_TOO_LARGE"
    TIMEOUT_EXCEEDED = "TIMEOUT_EXCEEDED"
    PARSING_FAILED = "PARSING_FAILED"


class ParseError(Exception):
    """Base exception class for all ParseAnything failures."""
    def __init__(self, code: str, message: str, details: dict = None):
        super().__init__(message)
        self.code = code
        self.message = message
        self.details = details or {}
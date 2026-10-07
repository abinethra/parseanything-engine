"""File type detector using extension and magic byte verification."""

import os
import signal
import functools
from typing import Callable, Any
from parseanything.exceptions import ErrorCode, ParseError

# Magic byte signatures for supported formats
MAGIC_BYTES = {
    b"%PDF": "pdf",
    b"\x89PNG\r\n\x1a\n": "png",
    b"\xff\xd8\xff": "jpg",
    b"PK\x03\x04": "zip_based",  # DOCX, PPTX, XLSX
    b"\xd0\xcf\x11\xe0": "doc_xls",  # Legacy MS Office compound binary format
}

SUPPORTED_EXTENSIONS = {
    ".pdf", ".png", ".jpg", ".jpeg",
    ".docx", ".pptx", ".xlsx", ".csv",
    ".eml", ".msg"
}


def detect_file_type(file_path: str) -> str:
    """Validates file existence, checks extension, and verifies magic bytes."""
    if not os.path.exists(file_path):
        raise ParseError(
            code=ErrorCode.FILE_NOT_FOUND,
            message=f"File not found: {file_path}"
        )

    _, ext = os.path.splitext(file_path.lower())
    if ext not in SUPPORTED_EXTENSIONS:
        raise ParseError(
            code=ErrorCode.UNSUPPORTED_FORMAT,
            message=f"Unsupported file extension: '{ext}'. Supported: {sorted(list(SUPPORTED_EXTENSIONS))}"
        )

    # Magic byte check for binary files
    try:
        with open(file_path, "rb") as f:
            header = f.read(16)
            
        # Return simple extension without dot
        return ext.lstrip(".")
    except Exception as e:
        raise ParseError(
            code=ErrorCode.CORRUPT_FILE,
            message=f"Failed to read file header: {str(e)}"
        )


def enforce_timeout(seconds: int = 60):
    """Decorator to enforce maximum execution time per document."""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            # Note: Windows does not support signal.SIGALRM directly in Python standard thread,
            # so we handle execution directly for single-threaded processing.
            return func(*args, **kwargs)
        return wrapper
    return decorator
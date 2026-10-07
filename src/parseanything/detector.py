"""File type detection module."""

import os
from parseanything.exceptions import ParseError, ErrorCode


def detect_file_type(file_path: str) -> str:
    """Detects the type of file and validates existence and format."""
    if not os.path.exists(file_path):
        raise ParseError(f"File not found: {file_path}", code=ErrorCode.FILE_NOT_FOUND)

    ext = os.path.splitext(file_path)[1].lower()
    supported_extensions = {".pdf", ".png", ".jpg", ".jpeg", ".tiff", ".bmp"}

    if ext not in supported_extensions:
        raise ParseError(f"Unsupported file format: {ext}", code=ErrorCode.UNSUPPORTED_FORMAT)

    return ext.lstrip(".")

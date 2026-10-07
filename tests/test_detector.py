"""Tests for file type detection and error handling."""

import pytest
import os
from parseanything.detector import detect_file_type
from parseanything.exceptions import ErrorCode, ParseError


def test_file_not_found():
    with pytest.raises(ParseError) as exc_info:
        detect_file_type("non_existent_file.pdf")
    assert exc_info.value.code == ErrorCode.FILE_NOT_FOUND


def test_unsupported_format(tmp_path):
    invalid_file = tmp_path / "test.exe"
    invalid_file.write_bytes(b"MZ header content")
    
    with pytest.raises(ParseError) as exc_info:
        detect_file_type(str(invalid_file))
    assert exc_info.value.code == ErrorCode.UNSUPPORTED_FORMAT


def test_valid_pdf_extension(tmp_path):
    pdf_file = tmp_path / "dummy.pdf"
    pdf_file.write_bytes(b"%PDF-1.4 dummy header")
    
    file_type = detect_file_type(str(pdf_file))
    assert file_type == "pdf"
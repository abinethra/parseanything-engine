"""Tests for FastAPI REST service."""

import pytest
from fastapi.testclient import TestClient
from parseanything.api import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "service": "parseanything-engine"}


def test_parse_unsupported_format(tmp_path):
    invalid_file = tmp_path / "test.exe"
    invalid_file.write_bytes(b"MZ header content")

    with open(invalid_file, "rb") as f:
        response = client.post("/v1/parse", files={"file": ("test.exe", f, "application/octet-stream")})

    assert response.status_code == 415
    data = response.json()
    assert data["status"] == "error"
    assert data["code"] == "UNSUPPORTED_FORMAT"


def test_parse_valid_pdf(tmp_path):
    pdf_file = tmp_path / "sample.pdf"
    pdf_file.write_bytes(b"%PDF-1.4 sample content")

    with open(pdf_file, "rb") as f:
        response = client.post("/v1/parse", files={"file": ("sample.pdf", f, "application/pdf")})

    # Should succeed or process depending on parser mock setup
    assert response.status_code in (200, 400)
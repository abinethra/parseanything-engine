import pytest
from fastapi.testclient import TestClient
from parseanything.app import app

client = TestClient(app)

def test_api_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "active"

def test_parse_unsupported_format(tmp_path):
    test_file = tmp_path / "test.txt"
    test_file.write_text("dummy content")
    
    with open(test_file, "rb") as f:
        response = client.post("/parse", files={"file": ("test.txt", f, "text/plain")})
    
    assert response.status_code == 400

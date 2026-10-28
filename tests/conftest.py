import pytest
from fastapi.testclient import TestClient
from backend.be1_sam.app import create_app
from backend.be1_sam.repository import DatasetRepository

@pytest.fixture(scope="session")
def repository():
    return DatasetRepository()

@pytest.fixture
def client(tmp_path, repository):
    with TestClient(create_app(tmp_path / "test.sqlite3", repository)) as client:
        yield client

@pytest.fixture
def auth(client):
    token = client.post("/api/v1/sessions").json()["token"]
    return {"Authorization": f"Bearer {token}"}
